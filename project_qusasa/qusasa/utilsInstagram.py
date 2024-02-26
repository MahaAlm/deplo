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
import time
from instagrapi.mixins.challenge import ChallengeChoice
from dotenv import load_dotenv
load_dotenv()

USER_IG = os.environ.get("USER_IG")
PASS_IG = os.environ.get("PASS_IG")
EMAIL_ADD = os.environ.get("EMAIL_ADD")
PASS_EMAIL = os.environ.get("PASS_EMAIL")

def get_thumbnail_url(post_info):
    """
    Retrieves the thumbnail URL from a post_info dictionary.
    If the thumbnail URL is not available or None, it falls back to the first resource link.

    :param post_info: A dictionary containing post details, including 'thumbnail_url' and 'resources'.
    :return: A string containing the URL of the thumbnail or the first resource.
    """
    # Attempt to retrieve the thumbnail URL
    thumbnail_url = post_info.thumbnail_url
    
    # Check if the thumbnail URL is not None and not an empty string
    if thumbnail_url:
        return thumbnail_url
    
    # Fallback to the first resource link if the thumbnail URL is not available
    resources = post_info.resources
    if resources:
        # Assuming resources is a list of dictionaries and each has a 'url' key
        first_resource_url = resources[0].thumbnail_url
        if first_resource_url:
            return first_resource_url
    
    # Return None or a default value if neither thumbnail nor resources are available
    return None


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
    mail.login(EMAIL_ADD, PASS_EMAIL)  # Replace '****' with the actual password
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

        if msg.is_multipart():
            parts = msg.walk()
        else:
            parts = [msg]  # Treat as a single part for uniform handling
        for part in parts:
          content_type = part.get_content_type()
          print(f"Processing part with content type: {content_type}")  # Logging content type
          payload_data = part.get_payload(decode=True)

          if payload_data and (content_type == 'text/plain' or content_type == 'text/html'):
              body, used_encoding = decode_payload(payload_data)
              print(f"Decoded with encoding: {used_encoding}")  # Log used encoding

              # Your existing matching logic here
              if "<div" not in body:
                  continue
              match = re.search(">([^>]*?({u})[^<]*?)<".format(u=username), body)
              if match:
                  print("Match from email:", match.group(1))
                  match = re.search(r">(\d{6})<", body)
                  if match:
                      code = match.group(1)
                      return code
              else:
                  print('Skip this email, "code" not found')

          else:
              print("Payload data is None or content type is not text/plain or text/html.")

    return False

def challenge_code_handler(username, choice):
    if choice == ChallengeChoice.SMS:
        print('sms')
    elif choice == ChallengeChoice.EMAIL:
        return get_code_from_email(username)
    return False

def connectToInstaAPI():
    cl = Client()
    cl.challenge_code_handler = challenge_code_handler
    cl.login(USER_IG, PASS_IG)
    print('Connected to Instagram API')
    return cl
    
    

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


def postAnalysis(posturl):

    context = []
    listComm=[]
    commentDataset=[]
    cl = connectToInstaAPI()

    if cl:
            postCode = cl.media_pk_from_url(posturl)
            # Get post information
            post_info = cl.media_info(postCode)
            print(post_info)
            thumbnial_url = post_info.thumbnail_url
            icon_url = str(post_info.user.profile_pic_url)
            i = 0
            if thumbnial_url != None:
                print(thumbnial_url)
                cl.photo_download_by_url(str(thumbnial_url), 'thumbnial_url0', 'qusasa/static/qusasa/images')	
            else:
                resources = post_info.resources
                for post in resources:
                     cl.photo_download_by_url(str(post.thumbnail_url), f'thumbnial_url{i}', 'qusasa/static/qusasa/images')	
                     i = i+1
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
            
            num_pics = i
    else:
        time.sleep(120)
        cl = connectToInstaAPI()
        postAnalysis(posturl)

    return PostDf, commentDataset ,comment_sentiments, sentiments, num_pics# Print the post details



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
    import pandas as pd
    from keybert import KeyBERT
    # Assuming cl is already initialized and other necessary imports are done

    content = []
    creators = []
    hashAnalysis = []
    df = pd.DataFrame(columns=['text', 'pubDate', 'likeCount'])

        
    cl = connectToInstaAPI()

    hashtag = cl.hashtag_info(Hashtag)
    medias = cl.hashtag_medias_top(Hashtag, amount=numMedia)

    for media in medias:
        comments = cl.media_comments(media.pk, amount=1)
        comments_data = [{'text': comment.text, 'pubDate': comment.created_at_utc, 'likeCount': int(comment.like_count)} for comment in comments]
        temp_df = pd.DataFrame(comments_data)
        df = pd.concat([df, temp_df], ignore_index=True)
        thumbnailURL=get_thumbnail_url(media)

        post_info = {
            'postCode': media.code,
            'icon_url':str(media.user.profile_pic_url),
            'owner': media.user.username,
            'thumbnailURL':thumbnailURL,
            'caption': media.caption_text,
            'publishedAt': media.taken_at,  
            'likeCount': media.like_count,
            'CommentCount': media.comment_count,
            'saveCount': cl.insights_media(cl.media_pk_from_url('https://www.instagram.com/' + media.code + '/'))['save_count'],  
            'MediaType': map_media_type(media.media_type, getattr(media, 'product_type', None)),  
            'location': media.location,
        }
        content.append(post_info)
        



        dictMed = cl.user_info_by_username(media.user.username).model_dump()
        creator_info = {
            'creator': media.user.username,
            'icon_url':str(media.user.profile_pic_url),
            'bio': dictMed['biography'],
            'MediaCount': dictMed['media_count'],
            'followerCount': dictMed['follower_count'],
            'followingCount': dictMed['following_count'],
        }
        creators.append(creator_info)

    Recently = cl.hashtag_medias_recent(Hashtag, amount=1)[0].taken_at
    hashAnalysis.append({
        'hashtagID': hashtag.id,
        'hashtagName': hashtag.name,
        'media_count': hashtag.media_count,
        'lastPublishDate': parse_datetime(str(Recently)),
    })

    comments_text = " ".join(df['text'].tolist())
    kw_model = KeyBERT(model='all-MiniLM-L6-v2')
    keywords = kw_model.extract_keywords(comments_text, keyphrase_ngram_range=(1, 2), use_maxsum=True, nr_candidates=100, top_n=100)
    top_keywords = [keyword[0] for keyword in keywords]
    df['likeCount'] = pd.to_numeric(df['likeCount'], errors='coerce').astype('int')

    creators=pd.DataFrame(creators)
    content=pd.DataFrame(content)
    content.sort_values(by='likeCount', inplace=True, ascending=False)
    creators.sort_values(by='followerCount', inplace=True, ascending=False)

    hashAnalysis=pd.DataFrame(hashAnalysis)
    emotion_counts, top_comments_by_emotion=analyze_comments_emotions_for_playlist(df)
    top_6_posts = content.head(6).to_dict('records')
    top_5_accs = content.head(5).to_dict('records')

    i = 0
    for post in  top_6_posts:
        cl.photo_download_by_url(str(post['thumbnailURL']), f'thumbnial_url{i}', 'qusasa/static/qusasa/images/top_posts_insta')
        i = i + 1
    i = 0
    for acc in  top_5_accs:
        cl.photo_download_by_url(str(acc['icon_url']), f'icon_url{i}', 'qusasa/static/qusasa/images/top_posts_insta')
    return hashAnalysis, creators, content, df, top_keywords, emotion_counts, top_comments_by_emotion, top_6_posts, top_5_accs


