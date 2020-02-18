"""
Twitter API configuration module.
"""
from typing import List

from environs import Env


env = Env()
env.read_env()

# API Credentials.
CONSUMER_KEY: str = env.str('CONSUMER_KEY')
CONSUMER_SECRET: str = env.str('CONSUMER_SECRET')
ACCESS_TOKEN: str = env.str('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET: str = env.str('ACCESS_TOKEN_SECRET')

# Brake limits.
ACTION_BRAKE: int = 10
RATE_LIMIT_BREAK: int = 60

# Keywords.
prefix: str = 'python'
keywords: List[str] = [prefix, 'programming', 'developer', 'programmer',
                       'development']
KEYWORDS: List[str] = ([prefix+' '+keyword for keyword in keywords if
                        prefix not in keyword]+[prefix+keyword for keyword in
                                                keywords if
                                                prefix not in keyword]+keywords)

# Accounts.
ACCOUNTS_TO_WATCH: List[str] = []
