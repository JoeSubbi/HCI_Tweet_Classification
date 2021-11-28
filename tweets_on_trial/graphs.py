import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tweets_on_trial.settings')

import django
django.setup()
from app.models import Tweet, TweetResults
from plotly.offline import plot
import plotly.graph_objects as go # bar chart import
import plotly.express as px
import tkinter as tk

# Bar chart of total tweets
def get_total():
    results = TweetResults.objects.all()

    root = tk.Tk()
    width = root.winfo_screenwidth()

    d = {"Positive":0, "Neutral":0, "Aggressive":0, "Offensive":0, "Aggressive & Offensive":0}
    for result in results:
        m = result.mode()
        if d.get(m): d[m] += 1
        else: d[m] = 1
    
    fig = px.bar(x=list(d.keys()), y=list(d.values()), title="Model Opinion of All Categorised Tweets", labels=dict(x="Category", y="Number of Tweets"),
                 color=['#87de5f','#1f77b4', '#ed6b6b', '#ababab', '#f0a259'], color_discrete_map="identity")
    fig.update_layout(title_font_size=35, title_xanchor="left", paper_bgcolor="rgba(0,0,0,0)", width=width/1.5)
    
    fig.write_html("app/media/graphs/analytics/total_bar.html", full_html=False, include_plotlyjs='cdn')



# Compass of a single tweet, compared against others
def get_map(tweet):
    id = tweet.id
    
    # rated tweet data collection 
    n = TweetResults.objects.filter(tweet=tweet)[0].normalise().copy()
    tweet_body = Tweet.objects.get(id=tweet.id).body
    
    # other tweets data collection
    tweet_results_list = []
    tweet_body_list = []

    for results in TweetResults.objects.all():

        tweet_results_list.append(results.normalise().copy())

        tweet_body_list.append(Tweet.objects.get(id = results.id).body)

    # Remove important data, as it is overlayed on top

    tweet_results_list.remove(n)
    tweet_body_list.remove(tweet_body)

    aggressive_list = []
    offensive_list = []
    for i in range(len(tweet_results_list)):
        aggressive_list.append(tweet_results_list[range(len(tweet_results_list))[i]]["aggressive"])
        offensive_list.append(tweet_results_list[range(len(tweet_results_list))[i]]["offensive"])
    
    # create and format scatter plot
    root = tk.Tk()
    width = root.winfo_screenwidth()
    d = {'Aggressive': [0, 1], 'Offensive': [0, 1]}
    
    fig = px.scatter(title="Is the Tweet More Aggressive than Offensive?", width=width/2)
    fig.update_layout(yaxis_range=[0,1], xaxis_range=[0,1], title_font_size=25, title_xanchor="left", paper_bgcolor="rgba(0,0,0,0)", 
                      hovermode=None)
    
    # adding data to scatter plot
    fig.add_trace(go.Scatter(x=[n["aggressive"]], y=[n["offensive"]], mode="markers", name="Rated Tweet", hovertemplate=tweet_body, marker_color="crimson"))
    fig.add_trace(go.Scatter(x=aggressive_list, y=offensive_list, mode="markers", name="Other Tweets", hovertemplate=tweet_body_list, marker_color="#D3D3D3"))
    fig.update_traces(marker_size=20)
    fig.update_xaxes(title_text="Aggressive")
    fig.update_yaxes(title_text="Offensive")
    
    
    
    fig.write_html(f"app/media/graphs/map/{tweet.id}_map.html", full_html=False, include_plotlyjs='cdn')


# Bar chart of single tweet
def get_bar(tweet):
    id = tweet.id
    r = TweetResults.objects.filter(tweet=tweet)[0]
    x_list = ["Positive", "Neutral", "Aggressive", "Offensive"]
    y_list = [r.positive, r.neutral, r.aggressive, r.offensive]
    
    root = tk.Tk()
    width = root.winfo_screenwidth()
    
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