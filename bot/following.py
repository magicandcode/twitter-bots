"""
Twitter API bot module for follow and unfollow users.
"""
import time
from typing import Optional

import tweepy

from bot.logger import logger
from bot.config import RATE_LIMIT_BREAK, ACTION_BRAKE
from bot.utils import api_cursor, print_tweepy_error


def is_follower(api: tweepy.API, user_id: str) -> bool:
    """Checks if user is a follower."""
    friendship: Optional[tweepy.Friendship] = None
    if user_id.isnumeric():
        friendship = api.show_friendship(source_id=user_id,
                                         target_id=api.me().id_str)
    return friendship and friendship[0].following


def follow_user(api: tweepy.API, user_id: str):
    """Follow a user by id string or screen name."""
    try:
        user: tweepy.User = api.get_user(user_id)
        user.follow()
    except tweepy.TweepError as e:
        print_tweepy_error(e)


def unfollow_user(api: tweepy.API, user_id: str):
    """Unfollow a user by id string or screen name."""
    try:
        api.destroy_friendship(id=user_id)
    except tweepy.TweepError as e:
        print_tweepy_error(e)


def follow_followers(api: tweepy.API) -> None:
    """Follow all followers."""
    logger.info('Retrieving followers...')
    for follower in api_cursor(api.followers):
        logger.info(f'Follower: {follower.name} ({follower.screen_name})...')
        if not follower.following:
            try:
                follow_user(api, user_id=follower.id_str)
                logger.info(f'Following {follower.name} ('
                            f'{follower.screen_name})')
                time.sleep(ACTION_BRAKE)
            except tweepy.TweepError as e:
                print_tweepy_error(e)
                logger.info(f'Waiting {RATE_LIMIT_BREAK} seconds...')
                time.sleep(RATE_LIMIT_BREAK)


def unfollow_non_followers(api: tweepy.API) -> None:
    """Unfollow all non-followers."""
    logger.info('Retrieving followed users and checking relationships...')
    for friend in api_cursor(api.friends):
        logger.info(f'Currently following {friend.name} ('
                    f'{friend.screen_name})...')
        if not is_follower(api, user_id=friend.id_str):
            try:
                print('We are no longer friends. :(')
                unfollow_user(api, user_id=friend.id_str)
                logger.info(f'Unfollowing {friend.name} ('
                            f'{friend.screen_name})')
                time.sleep(ACTION_BRAKE)
            except tweepy.TweepError as e:
                print_tweepy_error(e)
                logger.info(f'Waiting {RATE_LIMIT_BREAK} seconds...')
                time.sleep(RATE_LIMIT_BREAK)
