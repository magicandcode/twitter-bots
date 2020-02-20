"""
Run Twitter bot, following followers and unfollowing ex followers.
"""
import time

from bots import create_api
from bots.following import unfollow_non_followers, follow_followers
from bots.config import RATE_LIMIT_BREAK


def main():
    """Create API instance and handle followers. Follow back any
     followers and unfollow ex followers.
    """
    api = create_api()
    while True:
        follow_followers(api)
        unfollow_non_followers(api)
        time.sleep(RATE_LIMIT_BREAK)


if __name__ == "__main__":
    main()
