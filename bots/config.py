"""
Twitter API configuration module.
"""
from typing import List, Set

from environs import Env


# environs.
env = Env()
env.read_env()


# API Credentials.
CONSUMER_KEY: str = env.str('CONSUMER_KEY')
CONSUMER_SECRET: str = env.str('CONSUMER_SECRET')
ACCESS_TOKEN: str = env.str('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET: str = env.str('ACCESS_TOKEN_SECRET')


# Brake limits.
ACTION_BRAKE: int = env.int('ACTION_BRAKE', 10)
RATE_LIMIT_BREAK: int = env.int('RATE_LIMIT_BREAK', 60)


# Keywords to track in stream.
PREFIX: str = env.str('KEYWORD_PREFIX', '')
KEYWORDS_TO_PREFIX: List[str] = env.list('KEYWORDS_TO_PREFIX', [])
PREFIXED_KEYWORDS: List[str] = [(PREFIX + ' ' + keyword).strip()
                                for keyword in KEYWORDS_TO_PREFIX]
KEYWORDS: Set[str] = set(PREFIXED_KEYWORDS + env.list('TRACKED_KEYWORDS', []))


# Mentions.
TRACK_MENTIONS: bool = env.bool('TRACK_MENTIONS', False)
MENTION_REPLY: str = env.str('MENTION_REPLY', 'Hi! 👋')


# Accounts to follow in stream.
ACCOUNTS_TO_WATCH: List[str] = env.list('ACCOUNTS_TO_WATCH', [])
