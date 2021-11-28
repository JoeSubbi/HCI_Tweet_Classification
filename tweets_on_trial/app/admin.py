from django.contrib import admin
from app.models import Tweet, TweetResults, UserProfile, UserTweetHistory

admin.site.register(Tweet)
admin.site.register(TweetResults)
admin.site.register(UserProfile)
admin.site.register(UserTweetHistory)
