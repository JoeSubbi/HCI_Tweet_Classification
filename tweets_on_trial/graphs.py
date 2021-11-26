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
import pyautogui

# Bar chart of total tweets
def get_total():
    tweets = Tweet.objects.all()
    results = TweetResults.objects.all()

    width, height= pyautogui.size()

    d = {}
    for result in results:
        m = result.mode()
        if d.get(m): d[m] += 1
        else: d[m] = 1
    
    fig = px.bar(x=list(d.keys()), y=list(d.values()), title="Model Opinion of All Categorised Tweets", labels=dict(x="Category", y="Number of Tweets"),
                 color=['#2ca02c', '#dc143c','#1f77b4', '#778899', '#ffa500'], color_discrete_map="identity")
    fig.update_layout(title_font_size=35, title_xanchor="left", paper_bgcolor="rgba(0,0,0,0)", width=width/1.5)
    
    fig.write_html("app/media/graphs/analytics/total_bar.html", full_html=False, include_plotlyjs='cdn')



# Compass of a single tweet
def get_map(tweet):
    id = tweet.id
    n = TweetResults.objects.filter(tweet=tweet)[0].normalise()
    
    width, height= pyautogui.size()

    x1 = n["aggressive"]
    y1 = n["offensive"]
    
    d = {'Aggressive': [0, 1], 'Offensive': [0, 1]}
    path = f"app/media/graphs/map/{tweet.id}_map.html"
    
    # create and format scatter plot
    fig = px.scatter(data_frame = d, x=[x1], y=[y1], title="Is this Tweet More Aggressive than Offensive?", labels=dict(x="Aggressive", y="Offensive"), width=width/2)
    fig.update_layout(yaxis_range=[0,1], xaxis_range=[0,1], title_font_size=25, title_xanchor="left", paper_bgcolor="rgba(0,0,0,0)")
    fig.update_traces(marker_size=20, marker_color='red')
    
    fig.write_html(path, full_html=False, include_plotlyjs='cdn')


# Bar chart of single tweet
def get_bar(tweet):
    id = tweet.id
    r = TweetResults.objects.filter(tweet=tweet)[0]
    x_list = ["Positive", "Neutral", "Aggressive", "Offensive"]
    y_list = [r.positive, r.neutral, r.aggressive, r.offensive]
    
    width, height= pyautogui.size()
    
    # create bar chart
    fig = px.bar(x=x_list, y=y_list, title="Summary of Opinions on this Tweet", labels=dict(x="Category", y="Number of Votes"), 
                 color=['#2ca02c', '#778899','#1f77b4',  '#dc143c'], color_discrete_map="identity", width=width/2)
    fig.update_layout(title_font_size=25, title_xanchor="left", paper_bgcolor="rgba(0,0,0,0)")
    
    fig.write_html(f"app/media/graphs/bar/{tweet.id}_bar.html", full_html=False, include_plotlyjs='cdn')
    

if __name__ == '__main__':
    for t in  Tweet.objects.all():
        get_map(t)
        get_bar(t)
    get_total()