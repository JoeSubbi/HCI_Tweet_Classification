from django.contrib import admin
from app.models import Tweet, TweetResults, UserProfile

admin.site.register(Tweet)
admin.site.register(TweetResults)
admin.site.register(UserProfile)
