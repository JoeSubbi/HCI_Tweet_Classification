import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tweets_on_trial.settings')

import django
django.setup()
from app.models import Tweet, TweetResults

import datetime
import matplotlib.pyplot as plt

from plotly.offline import plot
import plotly.graph_objects as go # bar chart import
import plotly.express as px
import pandas as pd

# Bar chart of total tweets
def get_total():
    tweets = Tweet.objects.all()
    results = TweetResults.objects.all()

    d = {}
    for result in results:
        m = result.mode()
        if d.get(m): d[m] += 1
        else: d[m] = 1
    
    fig = px.bar(x=list(d.keys()), y=list(d.values()))
    fig.write_html("app/media/graphs/analytics/total_bar.html", full_html=False, include_plotlyjs='cdn')



# Compass of a single tweet
def get_map(tweet):
    id = tweet.id
    n = TweetResults.objects.filter(tweet=tweet)[0].normalise()

    x1 = n["aggressive"]
    y1 = n["offensive"]
    
    d = {'col1': [0, 1], 'col2': [0, 1]}
    path = f"app/media/graphs/map/{tweet.id}_map.html"
    
    fig = px.scatter(data_frame = d, x=[x1], y=[y1], title="Aggression - Offensive graph")
    fig.update_layout(yaxis_range=[-1,1])
    fig.update_layout(xaxis_range=[-1,1])
    fig.update_traces(marker_size=20)
    fig.update_traces(marker_color='red')
    
    #fig.update_traces(text=tweet.body, selector=dict(type='scatter'))
    #fig.show()
    fig.write_html(path, full_html=False, include_plotlyjs='cdn')


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