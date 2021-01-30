"""
Twitter API streaming module with stream listener and helper functions.
"""
import time
import sys
from typing import Dict, Set

import tweepy

import bots.utils as utils
import bots.config as config
from bots.logger import logger


class BotStreamListener(tweepy.StreamListener):
    """Listen to stream and handle stream events."""

    def __init__(self, api: tweepy.API):
        super().__init__(api)
        self.since_id = 1

    @property
    def me(self) -> tweepy.User:
        """Get API user object."""
        return self.api.me()

    def is_mention(self, tweet: tweepy.Status) -> bool:
        """Check if a tweet is a mention."""
        return '@' + self.me.screen_name in tweet.text

    def reply_to_mention(self, tweet: tweepy.Status) -> None:
        """Reply to a mention."""
        status = f'@{tweet.user.screen_name} {config.MENTION_REPLY}'
        self.api.update_status(status=status,
                               in_reply_to_status_id=tweet.id_str,
                               auto_populate_reply_metadata=True)

    def is_own_tweet(self, tweet: tweepy.Status) -> bool:
        """Check if API user is author of tweet."""
        return tweet.user.id == self.me.id

    @staticmethod
    def retweet(tweet: tweepy.Status) -> None:
        """Retweet a tweet."""
        try:
            tweet.retweet()
        except tweepy.TweepError as e:
            utils.log_tweepy_error(e)

    @staticmethod
    def like(tweet: tweepy.Status) -> None:
        """Like a tweet."""
        try:
            tweet.favorite()
        except tweepy.TweepError as e:
            utils.log_tweepy_error(e)

    @staticmethod
    def on_friends(friends):
        # Todo: Implement method.
        logger.info(f'on_friends method triggered: {friends=}')

    def on_status(self, tweet: tweepy.Status) -> None:
        """Retweet and like matching tweets containing keywords and/or
         by accounts to watch.
        """
        try:
            # Return if tweet belongs to bot or is already checked.
            if self.is_own_tweet(tweet):
                return utils.log_stream_warning(
                    'This is your own tweet, ignore!')
            if tweet.id <= self.since_id:
                return logger.warning(
                    "You've already checked this tweet, ignore!")

            time.sleep(10)
            self.since_id = tweet.id
            logger.info(f'Current tweet:\n{tweet.text}')

            # Reply to mention.
            if tweet.in_reply_to_status_id is None and self.is_mention(tweet):
                self.reply_to_mention(tweet)
                logger.info(f'Replied to {tweet.user.screen_name}')
                print()
                time.sleep(10)
                return None

            # Like and retweet tracked tweets.
            self.like(tweet)
            time.sleep(0.1)
            self.retweet(tweet)
            time.sleep(0.1)

        except tweepy.TweepError as e:
            utils.log_tweepy_error(e)
        finally:
            print()

    @staticmethod
    def on_error(status_code):
        """Handle stream errors based on error status code."""
        if status_code == 420:
            print('Disconnected the stream')
            return False  # Disconnect stream
        if status_code == 429:
            logger.info('Waiting 120 seconds...')
            time.sleep(120)
        else:
            utils.log_tweepy_error(tweepy.TweepError)


def create(
    api: tweepy.API, timeout: int = config.STREAM_TIMEOUT,
) -> tweepy.Stream:
    """Get initialised stream."""
    return tweepy.Stream(
        auth=api.auth, listener=BotStreamListener(api=api), timeout=timeout)


def get_filter_params(api: tweepy.API) -> Dict[str, Set[str]]:
    """Return keywords and accounts to watch based on application
      settings.
    """
    keywords: Set[str] = config.KEYWORDS.copy()
    accounts: Set[str] = {api.get_user(user_id).id_str
                          for user_id in config.ACCOUNTS_TO_WATCH}
    if config.TRACK_HASHTAGS:
        keywords.update(config.HASHTAGS)
    if config.TRACK_MENTIONS:
        keywords.add('@' + api.me().screen_name)
    return {'keywords': keywords, 'accounts': accounts}


def filter(
    stream: tweepy.Stream,
    keywords,
    accounts,
    is_async: bool = config.STREAM_USES_MULTIPLE_THREADS,
) -> None:
    """Fetch and process tweets matching keywords and watched accounts.
    """
    try:
        stream.filter(
            track=keywords,
            follow=accounts,
            is_async=is_async,
        )
    except KeyboardInterrupt:
        stream.disconnect()
        print()
        logger.info('Exiting stream on user request, bye!')
        sys.exit()


if __name__ == '__main__':
    logger.info('Create and open a stream via the stream.py module.')
