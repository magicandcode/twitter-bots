"""
Run Twitter bot, following followers and unfollowing ex followers.
"""
import time

from bot import create_api
from bot.following import unfollow_non_followers, follow_followers
from bot.config import RATE_LIMIT_BREAK


def main():
    api = create_api()
    while True:
        follow_followers(api)
        unfollow_non_followers(api)
        time.sleep(RATE_LIMIT_BREAK)


if __name__ == "__main__":
    main()
