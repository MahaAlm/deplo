import pandas as pd
from dateutil import parser
import re
from collections import Counter
from transformers import pipeline, BertTokenizer, AutoModelForSequenceClassification
import torch
from instagrapi import Client
import torch
import pandas as pd
from collections import Counter
from transformers import pipeline, BertTokenizer, AutoModelForSequenceClassification
from keybert import KeyBERT
import os
from dotenv import load_dotenv
load_dotenv()

USER_IG = os.environ.get("USER_IG")
PASS_IG = os.environ.get("PASS_IG")
EMAIL = os.environ.get("EMAIL")
PASS_EMAIL = os.environ.get("PASS_EMAIL")

'''Photo - When media_type=1
Video - When media_type=2 and product_type=feed
IGTV - When media_type=2 and product_type=igtv
Reel - When media_type=2 and product_type=clips
Album - When media_type=8'''

import imaplib
import email
import re

def decode_payload(payload_data):
    """Attempt to decode payload with multiple encodings."""
    for encoding in ['utf-8', 'iso-8859-1', 'latin1']:
        try:
            return payload_data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return payload_data.decode('utf-8', 'ignore'), 'utf-8 (ignored errors)'

def get_code_from_email(username):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASS_EMAIL)  # Replace with the actual password
    mail.select("inbox")
    result, data = mail.search(None, "(UNSEEN)")
    if result != "OK":
        print("Error during get_code_from_email: %s" % result)
        return False
    ids = data[0].split()
    for num in reversed(ids):
        mail.store(num, "+FLAGS", "\\Seen")  # Mark as read
        result, data = mail.fetch(num, "(RFC822)")
        if result != "OK":
            print("Error fetching email: %s" % result)
            continue
        msg = email.message_from_bytes(data[0][1])

        code = None
        if msg.is_multipart():
            for part in msg.walk():
                code = process_part(part, username)
                if code:
                    break
        else:
            code = process_part(msg, username)  # Directly process if not multipart

        # Mark the email as unread after processing
        if code:
            mail.store(num, '-FLAGS', '\\Seen')  # Mark as unread
            print(f"Email marked as unread: {num}")
            return code

    return False

def process_part(part, username):
    content_type = part.get_content_type()
    print(f"Processing part with content type: {content_type}")  # Logging content type
    payload_data = part.get_payload(decode=True)
    if payload_data and (content_type == 'text/plain' or content_type == 'text/html'):
        body, used_encoding = decode_payload(payload_data)
        print(f"Decoded with encoding: {used_encoding}")  # Log used encoding

        # Existing matching logic
        if "<div" not in body:
            return
        match = re.search(">([^>]*?({u})[^<]*?)<".format(u=username), body)
        if match:
            print("Match from email:", match.group(1))
            match = re.search(r">(\d{6})<", body)
            if match:
                code = match.group(1)
                print(f"Code found: {code}")
                return code
        else:
            print('Skip this email, "code" not found')
    else:
        print("Payload data is None or content type is not text/plain or text/html.")

def connectToInstaAPI():

    cl = Client()
    try:
        cl.login(USER_IG, PASS_IG)
        print('Connected to Instagram API')
        return cl
    except Exception as e:
        print('Failed to connect:', str(e))
        return None
    
cl = connectToInstaAPI() 

def parse_datetime(datetime_str):
    parsed_datetime = parser.parse(datetime_str)
    formatted_datetime = parsed_datetime.strftime("%Y-%m-%d")

    return formatted_datetime

def analyze_comments_emotions_for_playlist(comments_df):

    tokenizer = BertTokenizer.from_pretrained('bhadresh-savani/bert-base-go-emotion')
    model = AutoModelForSequenceClassification.from_pretrained('bhadresh-savani/bert-base-go-emotion')

    # Function to safely analyze emotion (with truncation)
    def get_emotion(texts):
      # Ensure the input is a list of strings
      if isinstance(texts, str):
          texts = [texts]
      elif not isinstance(texts, list) or not all(isinstance(t, str) for t in texts):
          raise ValueError("Input must be a string or a list of strings.")

      # Tokenize and truncate texts
      inputs = tokenizer(texts, padding=True, truncation=True, max_length=512, return_tensors="pt")

      # Predict emotions
      with torch.no_grad():
          outputs = model(**inputs)
      logits = outputs.logits
      predictions = torch.argmax(logits, dim=-1)

      # Convert predictions to labels
      label = [model.config.id2label[prediction.item()] for prediction in predictions][0]
      return label

    # Add a new column to the DataFrame for the predicted emotions
    comments_df['emotion'] = comments_df['text'].apply(get_emotion)

    # Calculate the frequency of each emotion
    emotion_counts = comments_df['emotion'].value_counts(normalize=True)
    # Get the top 5 emotions
    top_emotions = emotion_counts.nlargest(5).index.tolist()

    # Create a dictionary to store the top comments for each emotion
    top_comments_by_emotion = {emotion: [] for emotion in top_emotions}

    # Get the top 5 comments for each of the top emotions
    for emotion in top_emotions:
        top_comments = comments_df[comments_df['emotion'] == emotion].nlargest(1, 'likeCount')
        top_comments_by_emotion[emotion] = top_comments['text'].iloc[0]


    return emotion_counts, top_comments_by_emotion

def map_media_type(media_type, product_type=None):
    """
    Map numerical media_type (and product_type for videos) to descriptive media type string.

    Args:
    - media_type (int): Numeric media type code from Instagram API.
    - product_type (str, optional): Additional descriptor for videos, if applicable.

    Returns:
    - str: Descriptive media type ('Photo', 'Video', 'IGTV', 'Reel', 'Album').
    """
    if media_type == 1:
        return 'Photo'
    elif media_type == 2:
        if product_type == 'feed':
            return 'Video'
        elif product_type == 'igtv':
            return 'IGTV'
        elif product_type == 'clips':
            return 'Reel'
        else:
            return 'Unknown Video Type'  # Fallback for unexpected product_type values
    elif media_type == 8:
        return 'Album'
    else:
        return 'Unknown'  # Fallback for unexpected media_type values

###########################################################################################################
###########################################################################################################

cl=connectToInstaAPI()

def postAnalysis(posturl):

    context = []
    listComm=[]
    commentDataset=[]

    if cl:
            postCode = cl.media_pk_from_url(posturl)
            # Get post information
            post_info = cl.media_info(postCode)
            print(post_info)
            thumbnial_url = str(post_info.thumbnail_url)
            icon_url = str(post_info.user.profile_pic_url)
            
            if thumbnial_url:
                cl.photo_download_by_url(thumbnial_url, 'thumbnial_url0', 'qusasa/static/qusasa/images')	
            else:
                resources = post_info.resources
                i = 0
                for post in resources:
                     cl.photo_download_by_url(str(post.thumbnail_url), f'thumbnial_url{i}', 'qusasa/static/qusasa/images')	
                     
            cl.photo_download_by_url(icon_url, 'icon_url', 'qusasa/static/qusasa/images')	
            
            # Get comments for the post
            comments = cl.media_comments(postCode,amount=post_info.comment_count)# the adjustment of the amount will affect the sentiment analysis
            for comment in comments:
              listComm.append([comment.text, comment.created_at_utc, comment.like_count])
            sortedListComm = sorted(listComm, key=lambda x: x[2], reverse=True)
            
            comments_text = " ".join(comment[0] for comment in listComm)

            kw_model = KeyBERT(model='all-MiniLM-L6-v2')

            keywords = kw_model.extract_keywords(comments_text, keyphrase_ngram_range=(1, 2), use_maxsum=True, nr_candidates=100, top_n=100)
            top_keywords = [keyword[0] for keyword in keywords]

            df = pd.DataFrame(listComm, columns=['text','pubDate','likeCount'])
            df.sort_values(by=['likeCount'])
            sentiments, comment_sentiments = analyze_comments_emotions_for_playlist(df)

            # Calculate sentiment percentages

            dictMed=cl.user_info_by_username(post_info.user.username).model_dump()
            
            context.append({
                'postID': postCode,
                'thumbnial_url': thumbnial_url,
                'icon_url': icon_url,
                'owner':post_info.user.username,
                'MediaCount':dictMed['media_count'],
                'followerCount': dictMed['follower_count'],
                'followingCount': dictMed['following_count'],
                'caption':post_info.caption_text,
                'publishedAt':parse_datetime(str(post_info.taken_at)),
                'LikeCount': post_info.like_count,
                'CommentCount': post_info.comment_count,
                'MediaType':map_media_type(post_info.media_type, getattr(post_info, 'product_type', None)),
                'top_keywords': top_keywords
            })
            
            PostDf = pd.DataFrame(context)


            commentDataset.append({
              'Comment': [comment[0] for comment in sortedListComm],
              'CommentDate': [parse_datetime(str(comment[1])) for comment in sortedListComm],
              'CommentLikes': [comment[2] for comment in sortedListComm]
          })

    return PostDf, commentDataset ,comment_sentiments, sentiments  # Print the post details



def commentDatasetToDF(commentDataset,context):
  dfcom = pd.DataFrame({
      'Comment': commentDataset[0]['Comment'],
      'CommentDate': commentDataset[0]['CommentDate'],
      'CommentLikes': commentDataset[0]['CommentLikes']
  })
  dfConr=pd.DataFrame(context)
  dfcom=dfcom.drop_duplicates()
  return dfcom, dfConr

###########################################################################################################
###########################################################################################################


def topicAnalysis(Hashtag, numMedia):
    content = []
    creators = []
    hashAnalysis = []
    
    try:
        hashtag = cl.hashtag_info(Hashtag)
        medias = cl.hashtag_medias_top(Hashtag, amount=numMedia)
    except Exception as e:
        return f"Failed to fetch hashtag info or top medias: {e}", [], []
    
    for media in medias:
        try:
            post_info = {
                'postCode': media.code,
                'owner': media.user.username,
                'caption': media.caption_text,
                'publishedAt': parse_datetime(str(media.taken_at)),
                'LikeCount': media.like_count,
                'CommentCount': media.comment_count,
                'saveCount': cl.insights_media(cl.media_pk_from_url('https://www.instagram.com/' + media.code + '/'))['save_count'],
                'MediaType': map_media_type(media.media_type, getattr(media, 'product_type', None)),
                'location': media.location,
            }
            content.append(post_info)
        except Exception as e:
            content.append(f"Failed to process media {media.code}: {e}")

        try:
            dictMed = cl.user_info_by_username(media.user.username).model_dump()
            creator_info = {
                'creator': media.user.username,
                'bio': dictMed['biography'],
                'MediaCount': dictMed['media_count'],
                'followerCount': dictMed['follower_count'],
                'followingCount': dictMed['following_count'],
            }
            creators.append(creator_info)
        except Exception as e:
            creators.append(f"Failed to fetch user info for {media.user.username}: {e}")

    try:
        Recently = cl.hashtag_medias_recent(Hashtag, amount=1)[0].taken_at
        hashAnalysis.append({
            'hashtagID': hashtag.id,
            'hashtagName': hashtag.name,
            'media_count': hashtag.media_count,
            'lastPublishDate': parse_datetime(str(Recently))
        })
    except Exception as e:
        hashAnalysis.append(f"Failed to fetch recent media info: {e}")

    return hashAnalysis, creators, content

###########################################################################################################
###########################################################################################################

