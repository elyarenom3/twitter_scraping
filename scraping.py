import tweepy
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
client = tweepy.Client(bearer_token=bearer_token)


def fetch_tweets_v2(username, max_results=100):
    try:
        user = client.get_user(username=username)
        user_id = user.data.id
    except tweepy.TweepyException as e:
        print(f"Error fetching user {username}: {e}")
        return []

    try:
        tweets = client.get_users_tweets(id=user_id, max_results=max_results, tweet_fields=['created_at', 'public_metrics', 'entities'])
    except tweepy.TweepyException as e:
        print(f"Error fetching tweets for user {username}: {e}")
        return []

    data = []
    if tweets.data:
        for tweet in tweets.data:
            tweet_data = {
                'id': tweet.id,
                'created_at': tweet.created_at,
                'text': tweet.text,
                'retweet_count': tweet.public_metrics['retweet_count'],
                'like_count': tweet.public_metrics['like_count'],
                'hashtags': [hashtag['tag'] for hashtag in tweet.entities.get('hashtags', [])],
                'mentions': [mention['username'] for mention in tweet.entities.get('mentions', [])],
                'photos': [media['url'] for media in tweet.entities.get('media', []) if media['type'] == 'photo']
            }
            data.append(tweet_data)
    else:
        print(f"No tweets found for user: {username}")
    return data


# List of Twitter accounts to scrape
accounts = ['davidattenburro']

all_tweets = []
for account in accounts:
    all_tweets.extend(fetch_tweets_v2(account))

df = pd.DataFrame(all_tweets)

df.to_csv('tweets_data.csv', index=False)
print('Tweets have been saved to tweets_data.csv')
