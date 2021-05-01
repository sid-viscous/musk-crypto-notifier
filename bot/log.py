import json
import os
import logging
from discord_handler import DiscordHandler

LOG_FORMAT = logging.Formatter("%(asctime)s - %(name)-6s - %(levelname)-7s - %(message)s")
TWEET_FORMAT = logging.Formatter("%(message)s")


class Logger:

    def __init__(self, logging_agent, logs_webhook_url=None, tweets_webhook_url=None, offline_mode=True):
        self.test_mode = os.getenv("TEST_MODE", default=True)

        # Initialise logger
        self.logger = logging.getLogger(logging_agent)
        self.logger.setLevel(logging.DEBUG)

        # Define console handler and add to logger
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(LOG_FORMAT)
        self.logger.addHandler(console_handler)

        if not offline_mode:
            # Define discord handler and add to logger
            discord_log_handler = DiscordHandler(logs_webhook_url, emit_as_code_block=False)
            discord_log_handler.setLevel(logging.DEBUG)
            discord_log_handler.setFormatter(LOG_FORMAT)
            self.logger.addHandler(discord_log_handler)

            # If webhook for tweets has been supplied, define discord handler and add it to logger
            if tweets_webhook_url:
                tweet_format = TWEET_FORMAT
                discord_tweet_handler = DiscordHandler(tweets_webhook_url, logging_agent, emit_as_code_block=False)
                discord_tweet_handler.setLevel(logging.INFO)
                discord_tweet_handler.setFormatter(tweet_format)
                self.logger.addHandler(discord_tweet_handler)

    def log(self, message, level="info"):
        if level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "debug":
            self.logger.debug(message)

    def info(self, message):
        self.log(message, "info")

    def warning(self, message):
        self.log(message, "warning")

    def error(self, message):
        self.log(message, "error")

    def debug(self, message):
        self.log(message, "debug")
