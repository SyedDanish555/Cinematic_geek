import os
import random
import tweepy
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Twitter API credentials from environment variables
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

def get_random_media_path(folder):
    """Gets a random media (image/gif/video) path from the specified folder."""
    media_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov')
    media_files = [
        os.path.join(folder, f) for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(media_extensions)
    ]
    if not media_files:
        raise Exception("No media files found in folder")
    return random.choice(media_files)

def is_video(file_path):
    """Check if the file is a video based on its extension."""
    video_extensions = ('.mp4', '.mov')
    return file_path.lower().endswith(video_extensions)

def tweet_random_movie(api, client):
    """Selects a random movie folder, chooses a random media, and tweets it."""
    movie_folders = [f for f in os.listdir("db") if os.path.isdir(os.path.join("db", f))]
    if not movie_folders:
        raise Exception("No movie folders found")
    random_folder = random.choice(movie_folders)
    media_path = get_random_media_path(os.path.join("db", random_folder))
    movie_name = random_folder

    try:
        # Handle video upload differently from images/GIFs
        if is_video(media_path):
            media = api.media_upload(
                filename=media_path,
                media_category='tweet_video'
            )
            # Wait for video processing
            while media.processing_info['state'] in ['pending', 'in_progress']:
                time.sleep(media.processing_info.get('check_after_secs', 3))
                media = api.get_media_upload_status(media.media_id)
        else:
            # Handle images and GIFs
            media = api.media_upload(filename=media_path)
        
        media_id = media.media_id_string
        print(f"Media uploaded successfully. Media ID: {media_id}")

        # Tweet with the media
        status = f'{movie_name}'
        client.create_tweet(text=status, media_ids=[media_id])
        print("Successfully tweeted a random movie media.")
    except Exception as e:
        print(f"Error processing media or tweeting: {e}")

if __name__ == "__main__":
    # Authenticate with Twitter for API v1.1 (for media upload)
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Authenticate with Twitter for API v2 (for creating tweets)
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
        wait_on_rate_limit=True,
    )

    try:
        tweet_random_movie(api, client)
    except Exception as e:
        print(f"An error occurred: {e}")