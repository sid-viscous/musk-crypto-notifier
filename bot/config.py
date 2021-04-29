import tweepy
import logging
import os

from log import Logger

test_mode = os.getenv("TEST_MODE", default=True)

if test_mode:
    logs_webhook_url = os.getenv("DISCORD_TEST_LOGS_WEBHOOK_URL")
    tweets_webhook_url = os.getenv("DISCORD_TEST_TWEETS_WEBHOOK_URL")
    possible_tweets_webhook_url = os.getenv("DISCORD_TEST_LOGS_WEBHOOK_URL")
else:
    logs_webhook_url = os.getenv("DISCORD_LOGS_WEBHOOK_URL")
    tweets_webhook_url = os.getenv("DISCORD_TWEETS_WEBHOOK_URL")
    possible_tweets_webhook_url = os.getenv("DISCORD_LOGS_WEBHOOK_URL")

# Initiate loggers
logger = Logger('logs', logs_webhook_url)
tweet_logger = Logger('tweets', logs_webhook_url, tweets_webhook_url)
possible_tweet_logger = Logger('maybe', logs_webhook_url, possible_tweets_webhook_url)

# Get user id to follow - default to @elonmusk's id
following_id = os.getenv("TWITTER_USER_ID_TO_FOLLOW", "44196397")


def create_api():
    api_key = os.getenv("TWITTER_API_KEY")
    api_secret = os.getenv("TWITTER_API_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(
        auth,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True,
        retry_count=10,
        retry_delay=5
    )
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
