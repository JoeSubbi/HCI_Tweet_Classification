import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tweets_on_trial.settings')

import django
django.setup()
from app.models import Tweet, TweetResults, UserTweetHistory

import datetime

def populate():

    #deletes all objects from Car database table
    Tweet.objects.all().delete()
    TweetResults.objects.all().delete()
    UserTweetHistory.objects.all().delete()

    tweets = [
        {"body":"I'm so fucking happy",  
         "date": datetime.date(2021, 11, 17)},
        {"body":"fuck you joe subbiani", 
         "date": datetime.date(2021, 11, 15)},
        {"body":"Lets go to James' house and beat him up!", 
         "date": datetime.date(2021, 11, 17)},
        {"body":"Can't wait to get battered into this chippy", 
         "date": datetime.date(2021, 10,  9)},
        {"body":"Computing science students are disgusting sweaty nerds that live in their mums basement",
         "date": datetime.date(2021, 11, 16)},
        {"body":"My girlfriend is so fucking cute!",
         "date": datetime.date(2021, 11, 13)},
        {"body":"Damn, today has been a bit shit",
         "date": datetime.date(2021, 11, 17)},
    ]

    tweet_results = [
        {"positive" :15, # Positive
         "neutral"  :6,
         "aggressive":1,
         "offensive":2},

        {"positive" :2, # Offensive
         "neutral"  :1,
         "aggressive":7,
         "offensive":11},
        
        {"positive" :0, # Aggressive
         "neutral"  :1,
         "aggressive":19,
         "offensive":4},
        
        {"positive" :12, # Positive
         "neutral"  :8,
         "aggressive":2,
         "offensive":2},

        {"positive" :9, # Neutral
         "neutral"  :0,
         "aggressive":0,
         "offensive":9},
        
        {"positive" :17, # Positive
         "neutral"  :7,
         "aggressive":0,
         "offensive":7},

        {"positive" :0, # Both Agressive and Offensive
         "neutral"  :5,
         "aggressive":5,
         "offensive":5},
    ]
    for tweet, results in zip(tweets, tweet_results):
        t = add_tweet(tweet["body"], tweet["date"])
        add_results(t, results)

    for t in Tweet.objects.all():
        print(f' - {t} :')
        r = TweetResults.objects.filter(tweet=t)[0]
        print(f'{r}')

def add_tweet(body, date):
    t = Tweet.objects.get_or_create(body=body, date=date)[0]
    t.save()
    return t

def add_results(t, results):
    r = TweetResults.objects.get_or_create(tweet=t)[0]
    r.positive  = results["positive"]
    r.neutral   = results["neutral"]
    r.aggressive = results["aggressive"]
    r.offensive = results["offensive"]
    r.save()
    return r

if __name__ == '__main__':
    print("Starting Population Script")
    populate()