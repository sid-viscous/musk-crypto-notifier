import tweepy
import json
import os

from log import Logger

# =====================================================================
# SETTINGS
# =====================================================================
config = {
    "test_mode": os.getenv("TEST_MODE", "True").lower() in ("true", "1", "t"),
    "offline_mode": os.getenv("OFFLINE_MODE", "True").lower() in ("true", "1", "t"),
    "following_ids": os.getenv("TWITTER_USER_IDS_TO_FOLLOW", default="44196397").split(),
    "twitter_api_key": os.getenv("TWITTER_API_KEY"),
    "twitter_api_secret": os.getenv("TWITTER_API_SECRET"),
    "twitter_access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
    "twitter_access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
}

if config["test_mode"]:
    config["logs_webhook_url"] = os.getenv("DISCORD_TEST_LOGS_WEBHOOK_URL", default="")
    config["tweets_webhook_url"] = os.getenv("DISCORD_TEST_TWEETS_WEBHOOK_URL", default="")
    config["possible_tweets_webhook_url"] = os.getenv("DISCORD_TEST_LOGS_WEBHOOK_URL", default="")
else:
    config["logs_webhook_url"] = os.getenv("DISCORD_LOGS_WEBHOOK_URL")
    config["tweets_webhook_url"] = os.getenv("DISCORD_TWEETS_WEBHOOK_URL")
    config["possible_tweets_webhook_url"] = os.getenv("DISCORD_LOGS_WEBHOOK_URL")

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
def create_api():
    api_key = config["twitter_api_key"]
    api_secret = config["twitter_api_secret"]
    access_token = config["twitter_access_token"]
    access_token_secret = config["twitter_access_token_secret"]

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


# if config["offline_mode"]:
#     logger = Logger("logs", offline_mode=True)
#     tweet_logger = Logger("tweets", offline_mode=True)
#     possible_tweet_logger = Logger("maybe", offline_mode=True)
# else:
#     logger = Logger("logs", logs_webhook_url=config["log_webhook_url"])
#     tweet_logger = Logger("logs", logs_webhook_url=config["log_webhook_url"], tweets_webhook_url=config["tweets_webhook_url"])
#     possible_tweet_logger = Logger("logs", logs_webhook_url=config["log_webhook_url"], tweets_webhook_url=config["possible_tweets_webhook_url"])
