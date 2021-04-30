#!/usr/bin/env python
# tweepy-bot/bot/favretweet.py

import os
import tweepy
import logging
import json

from config import create_api, logger, tweet_logger, possible_tweet_logger, following_id
from brain import TweetHandler


class cryptoTweetListener(tweepy.StreamListener):

    def __init__(self, api):
        self.api = api
        self.me = api.me()
        self.tweet_handler = TweetHandler()


    def on_status(self, tweet):
        # The "follow" argument in the filter grabs all retweets and replies
        # To ensure, we only get tweets directly from the following account, apply an extra filter here
        if str(tweet.user.id) == following_id:
            logger.info(f"Processing tweet id {tweet.id} from {tweet.user.screen_name}")
            tweet_logger.info(tweet.text)

    def on_error(self, status):
        logger.error(status)
        return True



def main(keywords):
    api = create_api()
    tweets_listener = cryptoTweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(follow=[following_id])

if __name__ == "__main__":
    main(["Python", "Tweepy"])