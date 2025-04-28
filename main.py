import os
import random
import tweepy

# Your Twitter API credentials
api_key = "RDXQbuKaR54G76b19cfy5AYsG"
api_secret = "9p3S583MpL6QW3JLkemF0huhAqW4zguHLNzxbB7payLqC9zUqp"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAHg2uQEAAAAARzxFcNX1xAwlDl%2BQeAKeslKYdGA%3DlCiW1jOIzAucYTiQGfvadxxkBgXGB5YwOtVnMK8XkDj6jLRb8v"
access_token = "1717632272038576128-KID7HyB2RqLDk3jHGod1p1sEJ5lYxU"
access_token_secret = "yhxTrqiW1p3jfYwtcpNKhP3E3ZyyxmCAdxEaaLAalCZ5N"

def get_random_image_path(image_folder):
    """Gets a random image path from the specified folder."""
    images = [os.path.join(image_folder, image) for image in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, image))]
    if not images:
        raise Exception("No images found in folder")
    return random.choice(images)

def tweet_random_movie(api, client):
    """Selects a random movie folder, chooses a random image, and tweets it."""
    movie_folders = [f for f in os.listdir("db") if os.path.isdir(os.path.join("db", f))]
    if not movie_folders:
        raise Exception("No movie folders found")
    random_folder = random.choice(movie_folders)
    image_path = get_random_image_path(os.path.join("db", random_folder))
    movie_name = random_folder

    # Upload the image and get the media ID
    try:
        media = api.media_upload(filename=image_path)
        media_id = media.media_id_string
        print(f"Image uploaded successfully. Media ID: {media_id}")
    except Exception as e:
        print(f"Error uploading media: {e}")
        return

    # Tweet the movie name with the image using Twitter API v2
    status = f'{movie_name}'
    try:
        client.create_tweet(text=status, media_ids=[media_id])
        print("Successfully tweeted a random movie.")
    except Exception as e:
        print(f"Error tweeting: {e}")

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