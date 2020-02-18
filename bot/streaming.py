"""
Twitter API streaming module with stream listeners.
"""
import time

import tweepy

import bot.utils
import bot.config


class BotStreamListener(tweepy.StreamListener):
    """Handle stream events."""
    def __init__(self, api: tweepy.API):
        super().__init__(api)

    @property
    def me(self) -> tweepy.API:
        return self.api.me()

    def on_friends(self, friends):
        pass

    def on_status(self, tweet):
        """Print new tweet if it contains keywords and or its author is
         in the accounts to watch.
        """
        print(f"{tweet.user.name}:\n{tweet.text}")

    def on_error(self, status_code):
        """Handle errors in stream."""
        if status_code == 420:
            return False  # Disconnect stream
        elif status_code == 429:
            time.sleep(120)
        else:
            e = tweepy.TweepError
            print(e, f'(Status code: {status_code})')


def get_stream(api: tweepy.API):
    """Get initialised stream."""
    return tweepy.Stream(auth=api.auth, listener=BotStreamListener(api=api))


def filter_stream(api:  tweepy.API) -> None:
    """Fetch and process tweets matching keywords and accounts."""
    stream = get_stream(api)
    stream.filter(track=bot.config.KEYWORDS,
                  follow=bot.config.ACCOUNTS_TO_WATCH)


if __name__ == '__main__':
    pass
