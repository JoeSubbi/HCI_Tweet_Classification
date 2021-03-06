from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from app.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from app.models import Tweet, TweetResults, UserTweetHistory
from datetime import datetime, timedelta
from random import randint
import json
import graphs 

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    context_dict = {}
    graphs.get_total()
    with open("app/media/graphs/analytics/total_bar.html","r") as f:
        graph_html = f.read()

    context_dict['totalbar'] = graph_html
    
    return render(request, 'app/index.html', context=context_dict)

def judge(request):

       # Tweets user has already voted on
    user = request.user
    if user.is_anonymous:
        return HttpResponse("Not logged in")
    
    
    

    if request.is_ajax and request.method == 'POST':

        print(request.POST.get('tweetId'))

        tweet = Tweet.objects.get(id =request.POST.get('tweetId'))
        isNegative = request.POST.get('isNegative')
        inputJudgement = request.POST.get('inputJudgement')

        tweetResults = TweetResults.objects.get(tweet=tweet)

        if inputJudgement == '0':

                #handle skip#
                print("skipped")
                hist = UserTweetHistory.objects.create(user = user, tweet=tweet, judgement="Skipped")
                hist.save()
                response = {    'redirect': True,
                                'redirect_url': reverse('app:stats', kwargs={'tweet_id': tweet.id}),
                                }
                print(response)
                return JsonResponse(response)
        elif isNegative:

            if inputJudgement == '1':

                #increment offensive
                tweetResults.incrementOff()
                hist = UserTweetHistory.objects.create(user = user, tweet=tweet, judgement="Offensive")
                hist.save()
                response = {    'redirect': True,
                                'redirect_url': reverse('app:stats', kwargs={'tweet_id': tweet.id}),
                                }
                print(response)
                return JsonResponse(response)

            elif inputJudgement == '2':

                #increment both
                tweetResults.incrementBoth()
                hist = UserTweetHistory.objects.create(user = user, tweet=tweet, judgement="Both")
                hist.save()
                response = {    'redirect': True,
                                'redirect_url': reverse('app:stats', kwargs={'tweet_id': tweet.id}),
                                }
                print(response)
                return JsonResponse(response)

            elif inputJudgement == '3':

                #increment aggressive
                tweetResults.incrementAgg()
                hist = UserTweetHistory.objects.create(user = user, tweet=tweet, judgement="Aggressive")
                hist.save()
                response = {    'redirect': True,
                                'redirect_url': reverse('app:stats', kwargs={'tweet_id': tweet.id}),
                                }
                print(response)
                return JsonResponse(response)
        else:
            if inputJudgement == '1':

                #increment positive
                tweetResults.incrementPos()
                hist = UserTweetHistory.objects.create(user = user, tweet=tweet, judgement="Positive")
                hist.save()
                response = {    'redirect': True,
                                'redirect_url': reverse('app:stats', kwargs={'tweet_id': tweet.id}),
                                }
                print(response)
                return JsonResponse(response)

            elif inputJudgement == '2':

                #increment neutral
                tweetResults.incrementNeut()
                hist = UserTweetHistory.objects.create(user = user, tweet=tweet, judgement="Neutral")
                hist.save()
                response = {    'redirect': True,
                                'redirect_url': reverse('app:stats', kwargs={'tweet_id': tweet.id}),
                                }
                print(response)
                return JsonResponse(response)

    else:

        tweets = UserTweetHistory.objects.filter(user=user)
    
        # Tweets within past 5 days
        DAYS = 100
        past = datetime.now() - timedelta(days=DAYS)
        tweets = Tweet.objects.exclude(id__in=[t.tweet.id for t in tweets]).filter(date__gte=past)
        
        if len(tweets) == 0:
            return HttpResponse("No more tweets right now, come back later")

        # Choose Random
        tweet = tweets[randint(0, len(tweets)-1)]

        # Load into context dict
    context_dict ={}
    #obj, created = Tweet.objects.get_or_create(body = "Can't wait to get battered into this chippy")
    context_dict['tweet'] = tweet
    tweetResults = TweetResults.objects.get(tweet=tweet)
    print(tweet)
    
    print(tweet.id)

    return render(request, 'app/judgement.html', context=context_dict)

def stats(request, tweet_id):
    try:
        intTweet = int(tweet_id)
        tweet = Tweet.objects.get(id=intTweet)
        results = TweetResults.objects.get(tweet=tweet)
        context_dict = {}
        context_dict['tweet'] = tweet
        context_dict['results'] = results
        
        
        graphs.get_map(tweet)
        graphs.get_bar(tweet)  

        
        with open(f"app/media/graphs/bar/{tweet.id}_bar.html","r") as f:
            bar_html = f.read()

        with open(f"app/media/graphs/map/{tweet.id}_map.html","r") as f:
            map_html = f.read()
            
        context_dict['barchart'] = bar_html
        context_dict['scatterplot'] = map_html
        
        return render(request, 'app/stats.html', context=context_dict)
    except Tweet.DoesNotExist:
        return HttpResponse("Tweet statistics not found")


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid:
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'app/register.html', context={'user_form': user_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('app:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'app/login.html')

@login_required
def user_logout(request):
    logout(request)

    return redirect(reverse('app:index'))

