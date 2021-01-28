"""
Twitter API search module with functions for retrieving matching items.
"""
from typing import List

import tweepy

from bots.utils import api_search_cursor


def get_tweets_containing_keywords(api: tweepy.API, query: List[str]):
    """Yield tweet matching search query."""
    yield from api_search_cursor(api, query)
