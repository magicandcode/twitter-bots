"""
Run Twitter bot, streaming matching tweets.
"""
from tweepy import API, Stream

from bots import create_api
from bots.streaming import create, filter, get_filter_params


def main():
    """Create API instance and open stream."""
    api: API = create_api()
    stream: Stream = create(api)
    filter(stream, **get_filter_params(api))


if __name__ == "__main__":
    main()
