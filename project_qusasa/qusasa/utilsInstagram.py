import pandas as pd
from datetime import timedelta
import re
from collections import Counter
from transformers import pipeline, BertTokenizer, AutoModelForSequenceClassification
import torch
from googleapiclient.errors import HttpErrors
from instagrapi import Client
import torch
import pandas as pd
from collections import Counter
from transformers import pipeline, BertTokenizer, AutoModelForSequenceClassification


'''Photo - When media_type=1
Video - When media_type=2 and product_type=feed
IGTV - When media_type=2 and product_type=igtv
Reel - When media_type=2 and product_type=clips
Album - When media_type=8'''


def connectToInstaAPI():

    cl = Client()
    try:
        cl.login('mahaalmua', 'Maha224')
        print('Connected to Instagram API')
        return cl
    except Exception as e:
        print('Failed to connect:', str(e))
        return None

cl=connectToInstaAPI()


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




def postAnalysis(postCode):
    context = []
    listComm=[]
    commentDataset=[]
    dictMed=dict(Photo=1,Video=2,IGTV=2,Reel=2,Album=8)
    if cl:
            # Get post information
            post_info = cl.media_info(postCode)

            # Get comments for the post
            comments = cl.media_comments(postCode,amount=post_info.comment_count)# the adjustment of the amount will affect the sentiment analysis
            for comment in comments:
              listComm.append([comment.text, comment.created_at_utc, comment.like_count])
            sortedListComm = sorted(listComm, key=lambda x: x[2], reverse=True)


            df = pd.DataFrame(listComm, columns=['text','pubDate','likeCount'])
            df.sort_values(by=['likeCount'])
            sentiments, comment_sentiments = analyze_comments_emotions_for_playlist(df)

            # Calculate sentiment percentages



            context.append({
                'postID': postCode,
                'owner':post_info.user.username,
                'caption':post_info.caption_text,
                'publishedAt':post_info.taken_at,
                'LikeCount': post_info.like_count,
                'CommentCount': post_info.comment_count,
                'MediaType':map_media_type(post_info.media_type, getattr(post_info, 'product_type', None)),
            })
            
            PostDf = pd.DataFrame(context)


            commentDataset.append({
              'Comment': [comment[0] for comment in sortedListComm],
              'CommentDate': [comment[1] for comment in sortedListComm],
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