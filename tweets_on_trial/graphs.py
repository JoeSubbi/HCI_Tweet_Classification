import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tweets_on_trial.settings')

import django
django.setup()
from app.models import Tweet, TweetResults

import datetime
import matplotlib.pyplot as plt

# Bar chart of total tweets
def get_total():
    tweets = Tweet.objects.all()
    results = TweetResults.objects.all()

    d = {}
    for result in results:
        m = result.mode()
        if d.get(m): d[m] += 1
        else: d[m] = 1

    plt.title("Modal opinion of all categorised tweets")
    plt.ylabel("Number of tweets")
    plt.xlabel("Category")
    plt.bar(x=d.keys(), height=d.values())
    plt.savefig("app/media/graphs/analytics/total_bar")
    plt.clf()

# Compass of a single tweet
def get_map(tweet):
    id = tweet.id
    n = TweetResults.objects.filter(tweet=tweet)[0].normalise()

    x = n["aggressive"]
    y = n["offensive"]

    plt.title("Summary of opinions on this tweet")
    plt.ylabel("Offensive",)
    plt.xlabel("Aggressive",)

    plt.plot(x,y, "ro")

    plt.xlim([0, 1])
    plt.ylim([0, 1])

    plt.savefig(f"app/media/graphs/map/{tweet.id}_map")
    plt.clf()

# Bar chart of single tweet
def get_bar(tweet):
    id = tweet.id
    r = TweetResults.objects.filter(tweet=tweet)[0]
    x = ["Positive", "Neutral", "Aggressive", "Offensive"]
    y = [r.positive, r.neutral, r.aggressive, r.offensive]

    plt.title("Summary of opinions on this tweet")
    plt.ylabel("Number of votes")
    plt.xlabel("Category")
    plt.bar(x, y)
    plt.savefig(f"app/media/graphs/bar/{tweet.id}_bar")
    plt.clf()

if __name__ == '__main__':
    for t in  Tweet.objects.all():
        get_map(t)
        get_bar(t)
    get_total()