import pandas as pd
from datetime import timedelta
import re
from collections import Counter
from transformers import pipeline

def searchByQuery(youtube, keyword, Type, orderBy='relevance', regionCode='', language=''):
    # Prepare the request with the parameters
    Max = 4
    
    request_parameters = {
        "part": "snippet",
        "order": orderBy,
        "q": keyword,
        "type": Type,
        "maxResults": Max
    }
    
    if(regionCode != ''):
        request_parameters["regionCode"] = regionCode
    
    if(language != ''):
        request_parameters["relevanceLanguage"] = language
    
    
        
    

    # Remove None values from request_parameters
    request_parameters = {k: v for k, v in request_parameters.items() if v is not None}

    request = youtube.search().list(**request_parameters)
    response = request.execute()
    result_list = []

    for item in response['items']:
        if Type == 'channel':
            result_list.append(item['id']['channelId'])
        elif Type == 'video':
            result_list.append(item['id']['videoId'])
        elif Type == 'playlist':
            playlist_id = item['id'].get('playlistId')
            if playlist_id is not None:
                result_list.append(playlist_id)
            else:
                print(f"Warning: 'playlistId' not found for item {item['snippet']}")

    return result_list

# Example usage
# r = searchByQuery('Minecraft', 'video', regionCode='US', language='en')

import re
def extractIdFromUrl(url):
    channel_pattern = r'youtube\.com/channel/([a-zA-Z0-9_-]+)'
    playlist_pattern = r'youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)'

    channel_match = re.search(channel_pattern, url)
    playlist_match = re.search(playlist_pattern, url)

    if channel_match:
        return channel_match.group(1)
    elif playlist_match:
        return playlist_match.group(1)
    else:
        return None


def get_videos_info(entity_id, youtube, entity_type='channel'):
    next_page_token = None
    unique_tags = set()
    category_count = Counter()
    total_likes = 0  # Initialize total likes
    total_views = 0  # Initialize total views
    name = None  # Initialize name variable
    video_data_list = []  # List to store video data
    top_video_info = None  # Initialize top video info
    durations = []
    # Determine the type of request based on entity type
    if entity_type == 'channel':
        playlist_id = youtube.channels().list(id=entity_id, part='contentDetails').execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    elif entity_type == 'playlist':
        playlist_id = entity_id
    else:
        raise ValueError("Invalid entity type. Must be 'channel' or 'playlist'.")

    # Fetch the videos
    while True:
        res = youtube.playlistItems().list(
            playlistId=playlist_id,
            part='contentDetails,snippet',
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        video_ids = [item['contentDetails']['videoId'] for item in res['items']]
        video_data_list.extend(res['items'])
        next_page_token = res.get('nextPageToken')
        if next_page_token is None:
            break

    top_views = 0  # Variable to store the highest number of views

    for video_id in video_ids:
        video_response = youtube.videos().list(part='statistics,contentDetails,snippet', id=video_id).execute()
        if 'items' in video_response and video_response['items']:
            video_details = video_response['items'][0]
            unique_tags.update(video_details['snippet'].get('tags', []))
            category_count[video_details['snippet']['categoryId']] += 1
            likes = int(video_details['statistics'].get('likeCount', 0))
            views = int(video_details['statistics'].get('viewCount', 0))
            total_likes += likes
            total_views += views
            duration = parse_duration_to_minutes(video_details['contentDetails'].get('duration'))
            durations.append(duration)
            # Check if this video has the most views
            if views > top_views:
                top_views = views
                top_video_info = {
                    'videoId': video_details['id'],
                    'title': video_details['snippet']['title'],
                    'description': video_details['snippet']['description'],
                    'thumbnail': video_details['snippet']['thumbnails']['high']['url'],
                    'viewsCount': views,
                    'likesCount': likes,
                    'duration': duration
                }

            # Set name if not already set
            if name is None:
                name = video_details['snippet']['channelTitle'] if entity_type == 'channel' else video_details['snippet']['title']

    average_likes = total_likes / len(video_data_list) if video_data_list else 0
    average_views = total_views / len(video_data_list) if video_data_list else 0


    # Convert category IDs to names
    category_names = {}
    category_ids = list(category_count.keys())
    if category_ids:
        category_response = youtube.videoCategories().list(part='snippet', id=','.join(category_ids)).execute()
        for item in category_response['items']:
            category_names[item['id']] = item['snippet']['title']

    most_used_categories = [(category_names.get(cid, 'Unknown'), count) for cid, count in category_count.most_common()]

    if top_video_info:
        # Fetch the top 3 comments for the most viewed video
        comments_response = youtube.commentThreads().list(part='snippet', videoId=top_video_info['videoId']).execute()
        comments = [comment['snippet']['topLevelComment']['snippet']['textDisplay'] for comment in comments_response['items']]
        top_comments = comments[:5]
        # Perform sentiment analysis on these comments
        comment_sentiments = analyze_sentiment(comments)
    
        # Calculate sentiment percentages
        sentiment_counts = Counter(comment_sentiments)
        total_comments = len(comment_sentiments)
        sentiment_percentages = {sentiment: count / total_comments for sentiment, count in sentiment_counts.items()}

        top_video_info['topComments'] = top_comments
        top_video_info['commentSentiments'] = sentiment_percentages


    return {
        'name': name,
        'topVideo': top_video_info,
        'durations': durations,
        'uniqueTags': list(unique_tags),
        'mostUsedCategories': most_used_categories,
        'averageLikes': average_likes,
        'averageViews': average_views,
        # 'videoData': video_data_list  # Optionally include detailed video data
    }



def parse_duration_to_minutes(duration):
    pattern = r'P(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
    match = re.match(pattern, duration)
    if match:
        days, hours, minutes, seconds = map(lambda x: int(x) if x else 0, match.groups())
        total_minutes = days * 24 * 60 + hours * 60 + minutes + seconds / 60
        return int(total_minutes)
    else:
        return 0

def analyze_sentiment(comments, max_length=512):
    # Load pre-trained model and tokenizer from Hugging Face
    sentiment_pipeline = pipeline("sentiment-analysis")

    # Truncate comments to the maximum length allowed by the model
    truncated_comments = [comment[:max_length] for comment in comments]

    # Analyze sentiment of each comment
    results = sentiment_pipeline(truncated_comments)

    # Extract sentiment labels from results
    sentiments = [result['label'] for result in results]
    return sentiments

def analyze_youtube_entity(entity_id, youtube, entity_type='channel'):
    data_list = []

    # Fetch entity information using the unified function
    videos_info = get_videos_info(entity_id, youtube, entity_type)
    categ = videos_info['mostUsedCategories']
    topTags = videos_info['uniqueTags'][:30]
    name = videos_info['name']
    topVideo = videos_info['topVideo']
    durations = videos_info['durations']
    mostUsedCategories = videos_info['mostUsedCategories']

    if entity_type == 'channel':
        # Fetch additional channel details
        request_entity = youtube.channels().list(part="snippet,statistics", id=entity_id)
        response_entity = request_entity.execute()

        if not response_entity['items']:
            return pd.DataFrame()  # Return an empty DataFrame if the channel is empty

        entity_stat = response_entity['items'][0]['statistics']
        entity_snippet = response_entity['items'][0]['snippet']
        channel_icon_url = entity_snippet['thumbnails']['high']['url']
        channel_url = f"https://www.youtube.com/channel/{entity_id}"


        # Calculate average views from the original viewCount
        view_average = int(entity_stat['viewCount']) / int(entity_stat['videoCount']) if int(entity_stat['videoCount']) > 0 else 0
        subscriber_count = entity_stat.get('subscriberCount', 0)

        request_playlists = youtube.playlists().list(part="snippet", channelId=entity_id)
        response_playlists = request_playlists.execute()
        playlist_count = response_playlists.get("pageInfo", {}).get("totalResults", 0)

        data_list.append([
            channel_url,
            name,
            view_average,
            videos_info['averageLikes'],
            categ,
            entity_stat['videoCount'],
            subscriber_count,
            topTags,
            mostUsedCategories,
            playlist_count
        ])
        columns = ['Channel URL', 'Name', 'View average', 'Like average', 'Categories', 'Video count', 'Subscriber count', 'Top tags', 'mostUsedCategories', 'Playlist count']
    else:  # For playlist
        # Use averageViews for playlists
        view_average = videos_info['averageViews']

        request_entity = youtube.playlists().list(part="snippet", id=entity_id)
        response_entity = request_entity.execute()

        # Fetch channel subscriber count
        channel_id = response_entity['items'][0]['snippet']['channelId']
        channel_response = youtube.channels().list(part="statistics", id=channel_id).execute()
        channel_stat = channel_response['items'][0]['statistics']
        subscriber_count = channel_stat.get('subscriberCount', 0)

        
        if not response_entity['items']:
            return pd.DataFrame()  # Return an empty DataFrame if the playlist is empty

        playlist_snippet = response_entity['items'][0]['snippet']
        channel_icon_url = playlist_snippet['thumbnails']['high']['url']
        channel_url = f"https://www.youtube.com/playlist?list={entity_id}"

        data_list.append([
            channel_url,
            name,
            view_average,
            videos_info['averageLikes'],
            categ,
            len(videos_info['durations']),
            subscriber_count,
            topTags,
            mostUsedCategories
        ])
        columns = ['Playlist URL', 'Name', 'View average', 'Like average', 'Categories', 'Video count', 'Subscriber count', 'Top tags', 'mostUsedCategories']

    df = pd.DataFrame(data_list, columns=columns)
    numeric_columns = ['View average', 'Like average', 'Video count', 'Subscriber count', 'Playlist count'] if entity_type == 'channel' else ['View average', 'Like average', 'Video count', 'Subscriber count']
    df[numeric_columns] = df[numeric_columns].round(2)

    return df, topVideo, channel_icon_url, durations

# # Example usage
# entity_id = id['id']  # Can be either a channel ID or a playlist ID
# entity_type = id['type']  # Change to "playlist" to analyze a playlist
# df, topVideo, channel_icon_url, durations = analyze_youtube_entity(entity_id, youtube, entity_type)


def analyse_channels(ids_list, entity_type, youtube): 
    channel_df_list = []  # List to store dataframes for each channel
    top_videos_list = []  # List to store top video data
    channel_icons_list = []  # List to store channel icons
    durations_list = []
    
    for id in ids_list:
        try:
            df, topVideo, channel_icon_url, durations = analyze_youtube_entity(id, youtube, entity_type)
            channel_df_list.append(df)
            top_videos_list.append(topVideo)
            channel_icons_list.append(channel_icon_url)
            durations_list.append(durations)
            
        except Exception as e:
            print(f"Error analyzing channel {id}: {str(e)}")

    # Concatenate the list of DataFrames vertically
    if channel_df_list:
        merged_channel_df = pd.concat(channel_df_list, ignore_index=True)
    else:
        print("No channel DataFrames to concatenate.")
        merged_channel_df = pd.DataFrame()

    # Convert top videos list to DataFrame
    if top_videos_list:
        top_videos_df = pd.DataFrame(top_videos_list)
    else:
        print("No top videos data to concatenate.")
        top_videos_df = pd.DataFrame()

    return merged_channel_df, top_videos_df, channel_icons_list, durations_list

