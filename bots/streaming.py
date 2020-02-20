"""
Twitter API streaming module with stream listener and helper functions.
"""
import time
from typing import List

import tweepy

import bots.utils
import bots.config
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
        return self.me.screen_name in tweet.text

    def reply_to_mention(self, tweet: tweepy.Status) -> None:
        """Reply to a mention, only if tweet is not a reply."""
        if tweet.in_reply_to_status_id is None and self.is_mention(tweet):
            status = f'@{tweet.user.screen_name} Hi fellow developer! 🐍'
            self.api.update_status(status=status,
                                   in_reply_to_status_id=tweet.id_str,
                                   auto_populate_reply_metadata=True)

    def is_my_tweet(self, tweet: tweepy.Status) -> bool:
        """Check if API user is author of tweet."""
        return tweet.user.id == self.me.id

    @staticmethod
    def retweet(tweet: tweepy.Status) -> None:
        """Retweet a tweet."""
        try:
            # Todo: Run try block without if condition?
            if not tweet.retweeted:
                tweet.retweet()
        except tweepy.TweepError as e:
            bots.utils.print_tweepy_error(e)

    @staticmethod
    def like(tweet: tweepy.Status) -> None:
        """Like a tweet."""
        try:
            # Todo: Run try block without if condition?
            if not tweet.favorited:
                tweet.favorite()
        except tweepy.TweepError as e:
            bots.utils.print_tweepy_error(e)

    def on_friends(self, friends):
        # Todo: Look up what kind of event this method handles.
        print('friends')
        print(friends)

    def on_status(self, tweet):
        """Print new tweet if it contains keywords and or its author is
         in the accounts to watch.
        """
        try:
            logger.info(f'Current since_id: {self.since_id}')
            logger.info(f'Current tweet id: {tweet.id}')
            if self.is_my_tweet(tweet) or tweet.id <= self.since_id:
                logger.warning(f"You've already checked this or it's your own"
                               ' tweet!')
                print('\n')
                return None

            self.since_id = tweet.id
            logger.info(f'Current tweet text: {tweet.text}')

            # Reply to mention.
            if self.me.screen_name.lower() in tweet.text.lower():
                self.reply_to_mention(tweet)
                logger.info(f'Replied to {tweet.user.screen_name}')
                print('\n')
                time.sleep(10)
                return None

            # Like and retweet tracked tweets.
            self.like(tweet)
            time.sleep(5)
            self.retweet(tweet)

            logger.info(f'New since_id: {self.since_id}')
            print('\n')
            time.sleep(10)
        except tweepy.TweepError as e:
            bots.utils.print_tweepy_error(e)

    def on_error(self, status_code):
        """Handle errors in stream."""
        if status_code == 420:
            print('Disconnected the stream')
            return False  # Disconnect stream
        elif status_code == 429:
            logger.info(f'Waiting 120 seconds...')
            time.sleep(120)
        else:
            e = tweepy.TweepError
            logger.info(f'{e} (Status code: {status_code})')


def get_stream(api: tweepy.API) -> tweepy.Stream:
    """Get initialised stream."""
    return tweepy.Stream(auth=api.auth, listener=BotStreamListener(api=api))


def filter_stream(api: tweepy.API, is_async: bool = True) -> None:
    """Fetch and process tweets matching keywords and accounts."""
    accounts: List[str] = [api.get_user(user_id).id_str for user_id in
                           bots.config.ACCOUNTS_TO_WATCH]
    stream = get_stream(api)
    stream.filter(track=bots.config.KEYWORDS, follow=accounts, is_async=is_async)


if __name__ == '__main__':
    logger.info(f'Create and open a stream via the stream.py module.')
