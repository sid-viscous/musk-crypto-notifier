""" Main routine for the Twitter listener.

Uses web sockets.

Initiates the Twitter listener, triggering the analysis methods when tweets are received.

"""
import time
import tweepy

from config import config, logger, twitter_api
from brain import TweetHandler


class CryptoTweetListener(tweepy.StreamListener):
    """ Crypto tweet listener.

    Listens for references to cryptocurrencies from specific users on Twitter.

    Attributes:
        api (API): Tweepy API instance.
        tweet_handler (TweetHandler): Tweet handler instance.

    """

    def __init__(self):
        """ Initialises Crypto tweet listener instance. """
        super().__init__()
        self.api = twitter_api()
        self.tweet_handler = TweetHandler()

    def on_status(self, tweet):
        """ Handles received new statuses (tweets).

        This class is overridden from Tweepy StreamListener and handles what to do when a new tweet is received.

        When a tweet is received from the watched user(s), it sends it to the the tweet handler for processing.

        Args:
            tweet (tweet): A tweet object containing tweet text and all metadata.
        """
        # The "follow" argument in the filter grabs all retweets and replies
        # To ensure, we only get tweets directly from the following account, apply an extra filter here
        if str(tweet.user.id) in config["following_ids"]:
            logger.info(f"Processing tweet id {tweet.id} from {tweet.user.screen_name}")
            logger.info(f"Tweet text: {tweet.text}")
            self.tweet_handler.process_tweet(tweet)

    def on_exception(self, exception):
        """ Handles exceptions encountered.

        Args:
            exception: Exception message.

        """
        logger.warning(f"An exception was found: {exception}")
        logger.info(f"Restarting API stream")
        main()

    def on_error(self, status):
        """ Handles errors received on the web socket.

        Args:
            status: Error status code.

        """
        if str(status) == "401":
            logger.warning("Incomplete read error at Twitter endpoint, will reconnect now.")
        elif str(status) == "420":
            logger.warning("Twitter API Rate Limit Exceeded, sleeping for 1 minute.")
            time.sleep(1 * 60)
        #else:
        #    logger.error(status)

        logger.info("Restarting API stream")
        main()


def main():
    """ Main function for running the bot. """
    logger.info("Starting Twitter feed listener")
    tweets_listener = CryptoTweetListener()
    stream = tweepy.Stream(tweets_listener.api.auth, tweets_listener)
    stream.filter(follow=config["following_ids"])


if __name__ == "__main__":
    main()
