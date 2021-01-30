"""
Run Twitter bot, following followers and unfollowing ex followers.
"""
import sys
import time

from bots import create_api
from bots.logger import logger
from bots.following import unfollow_non_followers, follow_followers
from bots.config import RATE_LIMIT_BREAK


def main():
    """Create API instance and handle followers. Follow back any
     followers and unfollow ex followers.
    """
    api = create_api()
    while True:
        try:
            follow_followers(api)
            unfollow_non_followers(api)
            time.sleep(RATE_LIMIT_BREAK)
        except KeyboardInterrupt:
            print()
            logger.info('Exiting polling on user request, bye!')
            sys.exit()


if __name__ == "__main__":
    main()
