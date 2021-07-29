""" Test script for running text analysis in offline mode """

import json
from brain import TweetHandler

class DictX(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<DictX ' + dict.__repr__(self) + '>'

texts = [
    "I am a tweet containing a BITCOin reference",
    "I refer to etherium",
    "I like CRYptocurrency",
    "I like doge, especially crypto, but not bitcoin",
    "I wish to take my dog to the moon today",
    "This tweet contains possible references, i.e. the moon and definite reference, i.e. bitcoin and doge",
    "@personwithbitcoinintheirhandle some text",
    "@anotherbitcoinperson actually talking about bitcoin"
    ]

tweets = []
i = 0

for text in texts:
    tweets.append(DictX({
        "id": i,
        "id_str": str(i),
        "text": text,
        "user": DictX({
            "id_str": "12345",
            "screen_name": "ghost"
        }),
        "entities": DictX({
            "media": []
        })
    }))
    i += 1

tweet_handler = TweetHandler()

for tweet in tweets:
    print("======================================")
    print(tweet)
    highlighted_text = tweet_handler.process_tweet(tweet)
    print(highlighted_text)
