"""
Run Twitter bot, streaming matching tweets.
"""
from bots import create_api
from bots.streaming import create_stream, filter_stream


def main():
    """Create API instance and open stream."""
    api = create_api()
    stream = create_stream(api)
    filter_stream(stream, api)


if __name__ == "__main__":
    main()
