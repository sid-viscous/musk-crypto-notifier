""" The brains of the operation.

This is where all the clever stuff happens:

    * Searching of keywords and possible keywords in text.
    * Highlighting keywords (using Discord markdown syntax).
    * Removing duplicate matches

"""

import json
import os
from fuzzysearch import find_near_matches
from google.cloud import vision
from config import config, tweet_logger, possible_tweet_logger, image_client, logger





class TweetHandler:
    """ Tweet handler.

    This class manages processing of tweets.

    Attributes:
        keywords (list of str): List of definite crypto keywords
        possible (list of str): List of possible crypto keywords
    """
    def __init__(self):
        self.keywords = config["keywords"]
        self.possible_keywords = config["possible_keywords"]
        self.possible_objects = config["possible_objects"]

    def _remove_duplicates(self, matches):
        """ Removes matches which are duplicated.

        For example, the text "I like etherium" could trigger keywords for "eth" and "etherium".

        This method removes the shortest duplicates.

        Args:
            matches: A list of keyword Matches

        Returns:
            A filtered list of keyword Matches containing no duplicates

        """
        for match_1 in matches:
            for match_2 in matches:
                if match_1.start == match_2.start and match_1 != match_2:
                    # 2 keywords start at the same position, find the shortest word and remove the match
                    logger.debug("These two keywords start at the same position: {} || {}".format(match_1, match_2))
                    if match_2.end >= match_1.end:
                        matches.remove(match_1)
                    else:
                        matches.remove(match_2)
                if match_1.end == match_2.end and match_1 != match_2:
                    # 2 keywords end at the same position, find the shortest word and remove the match
                    logger.debug("These two keywords start at the end position: {} || {}".format(match_1, match_2))
                    if match_2.start <= match_1.start:
                        matches.remove(match_1)
                    else:
                        matches.remove(match_2)
        return matches

    def _scan_text(self, keywords, text):
        """ Scans and finds keyword matches in text.

        Args:
            keywords (list of str): List of keywords to search for in the text
            text (str): Tweet text

        Returns:
            list of str: List of keywords found in the text.
        """
        # Remove handles from text
        text_no_handles = ' '.join(word for word in text.split(' ') if not word.startswith('@'))
        print("^^^")
        print(text_no_handles)

        # Scan for matches
        matches = []
        for keyword in keywords:
            if len(keyword) > 4:
                max_l_dist = 1
            else:
                max_l_dist = 0
            test = find_near_matches(keyword, text_no_handles, max_l_dist=max_l_dist)
            if test:
                matches.append(test[0])
        return self._remove_duplicates(matches)

    def scan_for_keywords(self, text):
        """ Scans for keywords in the text,

        Args:
            text (str): Tweet text.

        Returns:
            list of str: List of keywords found in the text.
        """
        return self._scan_text(self.keywords, text)

    def scan_for_possible_keywords(self, text):
        """ Scans for possible keywords in the text.

        Args:
            text (str): Tweet text.

        Returns:
            list of str: List of possible keywords found in the text.
        """
        return self._scan_text(self.possible_keywords, text)

    def scan_for_possible_image_objects(self, text):
        """ Scans for possible objects in the image.

        Args:
            text (str): Space delimited list of objects found in the image.

        Returns:
            list of str: List of possible objects found in the image..
        """
        return self._scan_text(self.possible_objects, text)

    def highlight_keywords(self, text, matches, bold=True, underline=True):
        """ Adds Discord compatible text highlighting.

        Args:
            text (str): String of the original tweet text in lower case.
            matches (list of str): List of keyword Matches.
            bold (bool): Boolean to set keywords bold.
            underline (bool): Boolean to set keywords underlined.

        Returns:
            str: A block of text containing Discord highlighting for the matched keywords.
        """

        if bold:
            start_block = "**"
            end_block = "**"
        else:
            start_block = ""
            end_block = ""
        if underline:
            start_block = "__" + start_block
            end_block = end_block + "__"

        for match in matches:
            # Get position of substring
            start = text.find(match.matched)
            end = start + len(match.matched)

            # Add the blocks to the string, starting with the end block
            # It is important to begin with the end block to avoid changing the position of the end of the string
            text = text[:end] + end_block + text[end:]
            text = text[:start] + start_block + text[start:]
        return text

    def build_tweet_url(self, tweet):
        """ Builds a link to the original tweet.

        Args:
            tweet: Instance of tweet object.

        Returns:
            str: A string containing the URL of the original tweet.

        """
        return f"http://twitter.com/{tweet.user.screen_name}/status/{tweet.id_str}"

    def message_formatter(self, intro, text, tweet):
        """ Sends results in standardised format.

        Args:
            intro (str): Intro text, e.g. "Possible", "Not a".
            text (str): Tweet text.
            tweet (tweet): Tweet object.

        Returns:
            str: A formatted string ready for logging.

        """
        return f"{intro} crypto related tweet from {tweet.user.screen_name}:\n \t{text}\n {self.build_tweet_url(tweet)}"

    def scan_image_text(self, image_url):
        """ Gets text from image.

        Uses Google Vision API to extract text from image.

        Args:
            image_url (str): Url for the image.

        Returns:
            str: A space delimited list of words in the image.

        """
        image = vision.Image()
        image.source.image_uri = image_url

        logger.info("Identifying text in image")
        response = image_client.text_detection(image=image)

        result = ""
        for text in response.text_annotations:
            temp = text.description.replace('\n', ' ').replace('\r', '')
            result = " ".join([result, temp])

        return result.lower()

    def scan_image_objects(self, image_url):
        """ Extracts objects from image.

        Uses Google Vision API to extract objects from the image, e.g. "car", "dog"

        Args:
            image_url (str): URL of the image.

        Returns:
            str: A space delimited string of objects found in the image.
        """
        image = vision.Image()
        image.source.image_uri = image_url
        response = image_client.label_detection(image=image)
        logger.info("Identifying objects in image:")

        result = ""
        for label in response.label_annotations:
            result = " ".join([result, label.description])

        return result.lower()

    def handle_keywords(self, tweet, text, matched_keywords, matched_possible_keywords):
        """ Checks if results exist for keywords and prints them.

        Logs are sent to the log handler.

        Args:
            tweet (tweet): Tweet object.
            text (str): Text where results were found, could be tweet text or image words.
            matched_keywords (list of str): List of matched crypto related keywords.
            matched_possible_keywords (list of str): List of possible matched crypto related keywords.

        """
        if matched_keywords:
            # Highlight the tweet text
            highlighted_text = self.highlight_keywords(text, matched_keywords)
            if matched_possible_keywords:
                highlighted_text = self.highlight_keywords(highlighted_text, matched_possible_keywords, bold=False)

            # Log tweet text
            tweet_logger.info(self.message_formatter("@everyone Matched", highlighted_text, tweet))

        elif matched_possible_keywords:
            # Highlight the tweet text
            highlighted_text = self.highlight_keywords(text, matched_possible_keywords, bold=False)

            # Log tweet text
            possible_tweet_logger.info(self.message_formatter("@everyone Possible", highlighted_text, tweet))

    def handle_objects(self, tweet, image_objects, matched_possible_image_objects):
        """ Checks if results exist for objects and prints them.

        Logs are sent to the log handler.

        Args:
            tweet (tweet): Tweet object.
            image_objects (str): Space delimited string containing objects found in the image.
            matched_possible_image_objects (list of str): List of possible matched objects found in the image.

        """
        if matched_possible_image_objects:
            # Highlight the objects
            highlighted_objects = self.highlight_keywords(image_objects, matched_possible_image_objects, bold=False)

            # Log list of objects
            possible_tweet_logger.info(self.message_formatter("@everyone Possible", f"Matched objects: {highlighted_objects}", tweet))

    def process_tweet(self, tweet):
        """ Main handler for tweets.

        Searches for keywords in the text and image.

        Also searches for objects, e.g. "dog", "animal".

        Uses Google Vision API for image analysis.

        Args:
            tweet (tweet): Tweet object

        """
        text = tweet.text.lower()

        # Get the keywords from the tweet text
        matched_keywords = self.scan_for_keywords(text)
        matched_possible_keywords = self.scan_for_possible_keywords(text)

        self.handle_keywords(tweet, text, matched_keywords, matched_possible_keywords)

        # Check if tweet contains an image
        try:
            for media in tweet.entities["media"]:
                if media["type"] == "photo":
                    logger.debug("Found image in tweet, sending to Google API for analysis")
                    image_url = media["media_url_https"]
                    logger.debug(image_url)
                    image_text = self.scan_image_text(image_url)
                    logger.info(f"Text in image: {image_text}")
                    image_objects = self.scan_image_objects(image_url)
                    logger.info(f"Objects in image: {image_objects}")
                    matched_image_keywords = self.scan_for_keywords(image_text)
                    matched_possible_image_keywords = self.scan_for_possible_keywords(image_text)
                    matched_possible_image_objects = self.scan_for_possible_image_objects(image_objects)

                    self.handle_keywords(tweet, image_text, matched_image_keywords, matched_possible_image_keywords)
                    self.handle_objects(tweet, image_objects, matched_possible_image_objects)
        except KeyError:
            pass
