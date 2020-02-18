"""
Twitter API utility functions module.
"""
import time
from typing import List

import tweepy

from bot.config import RATE_LIMIT_BREAK


def print_tweepy_error(e) -> None:
    """Format and print TweepError."""
    response = e.response
    print('Unable to create API!')
    print(response.reason)
    for error in response.json().get('errors'):
        print(f" > {error.get('message')} (code {error.get('code')})")


def limit_handler(cursor: tweepy.cursor.ItemIterator):
    """Sleep on RateLimitError."""
    try:
        while True:
            yield cursor.next()
    except tweepy.RateLimitError:
        print(f'RateLimit exceeded, waiting for {RATE_LIMIT_BREAK} seconds...')
        time.sleep(RATE_LIMIT_BREAK)
    except StopIteration:
        pass


def api_cursor(
    endpoint,
    limit=None,
    **kwargs
):
    """Get generator with API items."""
    if limit is None:
        limit = 100
    return limit_handler(cursor=tweepy.Cursor(endpoint, **kwargs).items(limit))


def api_search_cursor(
    api: tweepy.API,
    query: List[str],
    limit=None,
    **kwargs,
):
    """Get generator with tweets matching search query."""
    if limit is None:
        limit = 100
    return limit_handler(tweepy.Cursor(api.search, query, **kwargs).items(
                                       limit))
