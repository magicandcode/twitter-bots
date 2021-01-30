# Twitter Bots
### Testing and experimenting with the Twitter API (Standard 1.1)
![chatbot illustration](/../master/twitter-bots.png?raw=true "chatbot repository decorative illustration")

There are two bots: `poll.py` and `stream.py`.
### `poll.py`
This bot polls the Twitter API for its followers. It will follow any follower and unfollow ex-followers.
It does not use a stream but instead runs the function for following and unfollowing in an infinite `while` loop, sleeping at the end of each iteration to avoid exceeding the API rate limit.

### `stream.py`
This bot uses a stream to receive tweets from matching tracked sources in a live feed. It will ignore tweets where the API user is the author and handle other tweets accordingly;
* Reply to a mention which is not also a reply.
* Retweet and like any non-mentions from tracked sources.

## Hosting
The bots have been hosted and run on [Heroku](https://heroku.com/), on two free dynos.

## Prerequisites
You'll need a [Twitter developer account](https://developer.twitter.com/en/apply-for-access) to run the bots. Creating one is, unfortunately, not trivial. Be honest and say that you're trying out the API for developer and learning purposes. You'll also need a **website URL** to register a new app once your account is ready.

## Usage
I strongly recommend using a [virtual environment](https://docs.python.org/3/tutorial/venv.html).

Add your Twitter API credentials to `.env-sample` and set any additional settings according to the sample file and `config.py`. Save and rename the file to `.env`.
Once you've made the initial configurations, run each bot in a console with either `python -m poll` or `python -m stream`.

## Deployment
Deploying the bots on Heroku is almost as simple as following the official [Heroku Python guide](https://devcenter.heroku.com/articles/getting-started-with-python) on web apps.
The `Procfile` differs, and dynos won't start automatically when the process type is not `web`.
To run the bots, you need to `scale` the dynos from 0 to 1. The free tier on Heroku gives you access to two free dynos.
Scale-up dynos via the Heroku CLI:
```
$ heroku ps
Free dyno hours quota remaining this month: 550h 0m (100%)
Free dyno usage for this app: 0h 0m (0%)
For more information on dyno sleeping and how to upgrade, see:
https://devcenter.heroku.com/articles/dyno-sleeping

No dynos on ⬢ magicandcode-bot
$ heroku ps:scale stream=1
Scaling dynos... done, now running stream at 1:Free
$ heroku ps:scale poll=1
Scaling dynos... done, now running poll at 1:Free
```

Scale down dynos (take one or both bots offline):
```
$ heroku ps:scale stream=0
Scaling dynos... done, now running stream at 0:Free
$ heroku ps:scale poll=0
Scaling dynos... done, now running poll at 0:Free
```

Note that the instructions are tested on the macOS Terminal only. To use Windows CMD or Powershell, check the [official documentation](https://devcenter.heroku.com/articles/getting-started-with-python).

## Dependencies
* [python >= 3.7](https://www.python.org/downloads/)
* [tweepy](http://www.tweepy.org/) - Twitter API wrapper
* [environs](https://pypi.org/project/environs/) - Environment variables parsing

I use `environs`, but you can replace it with `python-dotenv`, `os.getenv` or similar. If you do, change the code in `config.py` to use your preferred package or module.

## Todo:
* Update to Twitter API v2
* Use a more modern API wrapper like [twython](https://pypi.org/project/twython/)

## Attributions
* Image by [mohamed Hassan](https://pixabay.com/users/mohamed_hassan-5229782/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3589528) [Pixabay](https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3589528)
