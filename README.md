# Twitter Bots
### Testing and experimenting with the Twitter API
![chatbot illustration](/../master/twitter-bots.png?raw=true "chatbot repository decorative illustration")

Currently there are two bots: `poll.py` and `stream.py`
### poll.py
This bot polls the Twitter API for its followers. It will follow any follower and unfollow ex followers.
It does not use a stream but rather runs the function for following and unfollowing in an infinite `while` loop, sleeping at the end of each iteration to not exceed the API rate limit.

### stream.py
This bot uses a stream to receive tweets form matching tracked sources in a live feed. It will ignore tweets where the API user is the author and handle other tweets accordingly;
* Reply to a mention which is not also a reply.
* Retweet and like any non-mentions from tracked sources.

### Hosting and installation
The code is hosted and run on [Heroku](https://heroku.com/), on two free dynos.

I strongly recommend using some kind of [virtual environment](https://docs.python.org/3/tutorial/venv.html).

If you want to run the bots with your own Twitter API credentials you need to export/set environmental variables according to `config.py`.
Once you've done that you simply run each bot in a console with either `python -m run` or `python -m stream`

Deploying on Heroku is almost as simple as following the official [Python guide](https://devcenter.heroku.com/articles/getting-started-with-python).
the `Procfile` differs and dynos won't be started automatically when the process type is other than `web`.
This means that in order to run the bots you need to `scale` the dynos from 0 to 1. The free tier on Heroku gives you access to two free dynos.
Scale up dynos via the Heroku CLI:
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

Note that this is only tested on macOS. For Windows CMD or Powershell do I refer to the [official documentation](https://devcenter.heroku.com/articles/getting-started-with-python).


### Dependencies
* [python >= 3.7](https://www.python.org/downloads/)
* [tweepy](http://www.tweepy.org/) - Twitter API wrapper
* [environs](https://pypi.org/project/environs/) - Environment variables parsing

I use `environs` due to preference but it may be replaced with `os.getenv` or similar.

### Attributions
* Image by [mohamed Hassan](https://pixabay.com/users/mohamed_hassan-5229782/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3589528) [Pixabay](https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3589528)
