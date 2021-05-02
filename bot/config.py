""" Configuration settings for twitter notifier.

This module primarily extracts environment variables and places them into a single "config" dictionary.

Variables generally include application options, Twitter API authorisation, Discord webhooks etc.

Keywords for matching to tweets are also placed into the "config" dictionary here.

The API client and logging services are also set up here.

"""
import tweepy
import json
import os

from log import Logger

# =====================================================================
# SETTINGS
# =====================================================================
config = {
    "offline_mode": os.getenv("OFFLINE_MODE", "True").lower() in ("true", "1", "t"),
    "following_ids": os.getenv("TWITTER_USER_IDS_TO_FOLLOW", default="44196397").split(),
    "twitter_api_key": os.getenv("TWITTER_API_KEY"),
    "twitter_api_secret": os.getenv("TWITTER_API_SECRET"),
    "twitter_access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
    "twitter_access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    "logs_webhook_url": os.getenv("DISCORD_LOGS_WEBHOOK_URL", default=""),
    "tweets_webhook_url": os.getenv("DISCORD_TWEETS_WEBHOOK_URL", default=""),
    "possible_tweets_webhook_url": os.getenv("DISCORD_POSSIBLE_TWEETS_WEBHOOK_URL", default="")
}


# =====================================================================
# KEYWORDS
# =====================================================================
print(os.getcwd())
with open(os.path.join(os.getcwd(), "keywords.json")) as file:
    nlp_keywords = json.load(file)

config["keywords"] = nlp_keywords["keywords"]
config["possible_keywords"] = nlp_keywords["possible_keywords"]


# =====================================================================
# TWITTER API
# =====================================================================
def twitter_api():
    """ Creates client for Twitter API connection.

    Returns:
        API: Tweepy API instance.
    """
    auth = tweepy.OAuthHandler(config["twitter_api_key"], config["twitter_api_secret"])
    auth.set_access_token(config["twitter_access_token"], config["twitter_access_token_secret"])
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
        logger.error("Error creating API")
        raise e
    logger.info("API created")
    return api


# =====================================================================
# LOGGING
# =====================================================================
logger = Logger(
    "logs",
    logs_webhook_url=config["logs_webhook_url"],
    offline_mode=config["offline_mode"]
)
tweet_logger = Logger(
    "tweets",
    logs_webhook_url=config["logs_webhook_url"],
    tweets_webhook_url=config["tweets_webhook_url"],
    offline_mode=config["offline_mode"]
)
possible_tweet_logger = Logger(
    "possible_tweets",
    logs_webhook_url=config["logs_webhook_url"],
    tweets_webhook_url=config["possible_tweets_webhook_url"],
    offline_mode=config["offline_mode"]
)
