import json
from brain import TweetHandler

texts = [
    "I am a tweet containing a BITCOin reference",
    "I refer to etherium",
    "I like CRYptocurrency",
    "I like doge, especially crypto, but not bitcoin",
    "I wish to take my dog to the moon today",
    "This tweet contains possible references, i.e. the moon and definite reference, i.e. bitcoin and doge"
    ]

tweets = []
i = 0

for text in texts:
    tweets.append({
        "id": i,
        "text": text
    })
    i += 1

tweet_handler = TweetHandler()

for tweet in tweets:
    print("======================================")
    print(tweet)
    highlighted_text = tweet_handler.process_tweet(tweet)
    print(highlighted_text)
