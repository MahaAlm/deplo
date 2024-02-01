import googleapiclient.discovery
import os

def get_youtube_client():
    api_service_name = "youtube"
    api_version = "v3"
    
    # Access the API key from an environment variable
    DEVELOPER_KEY = "AIzaSyDU44aRiT2EzPoXmu66otL86PEFH0CIkqA"

    return googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
