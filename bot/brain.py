import json
import os
from fuzzysearch import find_near_matches
from config import config, tweet_logger, possible_tweet_logger, logger




class TweetHandler:
    def __init__(self):
        self.keywords = config["keywords"]
        self.possible_keywords = config["possible_keywords"]

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
        matches = []
        for keyword in keywords:
            test = find_near_matches(keyword, text, max_l_dist=0)
            if test:
                matches.append(test[0])
        return self._remove_duplicates(matches)

    def scan_for_keywords(self, text):
        return self._scan_text(self.keywords, text)

    def scan_for_possible_keywords(self, text):
        return self._scan_text(self.possible_keywords, text)

    def highlight_keywords(self, text, matches, bold=True, underline=True):
        """ Adds Discord compatible text highlighting.

        Args:
            text: String of the original tweet text in lower case.
            matches: List of keyword Matches .

        Returns:
            A block of text containing Discord highlighting for the matched keywords.

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
            # It is important to start with the end block to avoid changing the position of the end of the string
            text = text[:end] + end_block + text[end:]
            text = text[:start] + start_block + text[start:]
        return text

    def process_tweet(self, tweet):
        text = tweet.text.lower()

        # Get the keywords from the tweet text
        matched_keywords = self.scan_for_keywords(text)
        matched_possible_keywords = self.scan_for_possible_keywords(text)

        if matched_keywords:
            # Highlight the tweet text
            highlighted_text = self.highlight_keywords(text, matched_keywords)
            if matched_possible_keywords:
                highlighted_text = self.highlight_keywords(highlighted_text, matched_possible_keywords, bold=False)

            # Log tweet text
            tweet_logger.info(highlighted_text)

        elif matched_possible_keywords:
            # Highlight the tweet text
            highlighted_text = self.highlight_keywords(text, matched_possible_keywords, bold=False)

            # Log tweet text
            possible_tweet_logger.info(highlighted_text)

        else:
            logger.info("Not a crypto related tweet")







