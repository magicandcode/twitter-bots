"""
Twitter API setup module with functions for creating and authenticating
 a new API object based on the credentials in bot.config.
"""
import tweepy

import bot.utils
from bot.config import (ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY,
                        CONSUMER_SECRET, )


def create_api() -> tweepy.API:
    """Get authenticated api."""
    try:
        api: tweepy.API = tweepy.API(auth_handler=get_auth_handler(),
                                     wait_on_rate_limit=True,
                                     wait_on_rate_limit_notify=True)
        api.verify_credentials()
    except tweepy.TweepError as e:
        bot.utils.print_tweepy_error(e)
        exit(1)
    else:
        print(f'Tweepy API successfully created. Happy bot:ing'
              f' {api.me().name}!\n')
        return api


def get_auth_handler() -> tweepy.OAuthHandler:
    """Get OAuth handler."""
    auth: tweepy.OAuthHandler = tweepy.OAuthHandler(CONSUMER_KEY,
                                                    CONSUMER_SECRET)
    auth.set_access_token(key=ACCESS_TOKEN, secret=ACCESS_TOKEN_SECRET)
    return auth
