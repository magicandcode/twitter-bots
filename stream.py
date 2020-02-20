"""
Run Twitter bot, streaming matching tweets.
"""
from bots import create_api
from bots.streaming import filter_stream


def main():
    """Create API instance and open stream."""
    api = create_api()
    filter_stream(api, is_async=True)


if __name__ == "__main__":
    main()
