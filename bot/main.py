#!/usr/bin/env python
# tweepy-bot/bot/favretweet.py

import os
import tweepy
import logging
import json

from config import config, logger
from brain import TweetHandler


class cryptoTweetListener(tweepy.StreamListener):

    def __init__(self):
        self.api = self._create_api()
        self.me = self.api.me()
        self.tweet_handler = TweetHandler()

    def _create_api(self):
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
            logger.error("Error creating API", exc_info=True)
            raise e
        logger.info("API created")
        return api


    def on_status(self, tweet):
        # The "follow" argument in the filter grabs all retweets and replies
        # To ensure, we only get tweets directly from the following account, apply an extra filter here
        if str(tweet.user.id) in config["following_ids"]:
            logger.info(f"Processing tweet id {tweet.id} from {tweet.user.screen_name}")
            self.tweet_handler.process_tweet(tweet)

    def on_error(self, status):
        logger.error(status)
        return True



def main(keywords):
    tweets_listener = cryptoTweetListener()
    stream = tweepy.Stream(tweets_listener.api.auth, tweets_listener)
    stream.filter(follow=config["following_ids"])

if __name__ == "__main__":
    main(["Python", "Tweepy"])