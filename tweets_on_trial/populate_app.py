import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tweets_on_trial.settings')

import django
django.setup()
from app.models import Tweet, TweetResults

def populate():

    #deletes all objects from Car database table
    Tweet.objects.all().delete()
    TweetResults.objects.all().delete()

    tweets = [
        "I'm so fucking happy",
        "fuck you joe subbiani",
        "Lets go to James' house and beat him up!",
        "Can't wait to get battered into this chippy",
        "Computing science students are disgusting sweaty nerds that live in their mums basement",
        "My girlfriend is so fucking cute!",
        "Damn, today has been a bit shit",
    ]

    tweet_results = [
        {"positive" :15,
         "neutral"  :6,
         "agressive":1,
         "offensive":2},

        {"positive" :2,
         "neutral"  :1,
         "agressive":11,
         "offensive":7},
        
        {"positive" :0,
         "neutral"  :1,
         "agressive":19,
         "offensive":4},
        
        {"positive" :12,
         "neutral"  :8,
         "agressive":2,
         "offensive":2},

        {"positive" :9,
         "neutral"  :0,
         "agressive":0,
         "offensive":9},
        
        {"positive" :17,
         "neutral"  :7,
         "agressive":0,
         "offensive":7},

        {"positive" :0,
         "neutral"  :5,
         "agressive":5,
         "offensive":5},
    ]
    for body, results in zip(tweets, tweet_results):
        t = add_tweet(body)
        add_results(t, results)

    for t in Tweet.objects.all():
        print(f' - {t} :')
        r = TweetResults.objects.filter(tweet=t)[0]
        print(f'{r}')

def add_tweet(body):
    t = Tweet.objects.get_or_create(body=body)[0]
    t.save()
    return t

def add_results(t, results):
    r = TweetResults.objects.get_or_create(tweet=t)[0]
    r.positive  = results["positive"]
    r.neutral   = results["neutral"]
    r.agressive = results["agressive"]
    r.offensive = results["offensive"]
    r.save()
    return r

if __name__ == '__main__':
    print("Starting Population Script")
    populate()