"""
Twitter API bot module for replying to tweets.
"""
import time
from pprint import pprint
from typing import Optional

import tweepy

from bots.logger import logger
from bots.config import RATE_LIMIT_BREAK, ACTION_BRAKE
from bots.utils import api_cursor, print_tweepy_error


def reply_to_tweet(api: tweepy.API, tweet: tweepy.Status) -> None:
    #pprint(dir(tweet))
    #pprint(tweet)
    #pprint(tweet.__dict__)
    print('START OF NEW TWEET')
    pprint(tweet._json)
    print('\n\n')
    #pprint(tweet.retweets())
    #pprint(tweet[0])


def reply_to_mentions(api: tweepy.API):
    for tweet in api_cursor(api.mentions_timeline, limit=10):
        reply_to_tweet(api, tweet)
        time.sleep(4)
