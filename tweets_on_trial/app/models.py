from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.deletion import CASCADE

class Tweet(models.Model):
    body = models.CharField(max_length=256)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.body} -- {self.date}"

class TweetResults(models.Model):
    
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    positive  = models.IntegerField(default=0)
    neutral   = models.IntegerField(default=0)
    aggressive = models.FloatField(default=0)
    offensive = models.FloatField(default=0)

    valid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tweet.body}"\
               f"\tPositive:  {self.positive}\n"\
               f"\tNeutral:   {self.neutral}\n"\
               f"\tAggressive: {self.aggressive}\n"\
               f"\tOffensive: {self.offensive}"

    class Meta:
        verbose_name_plural = 'Tweet Results'

    def sum(self):
        return self.positive +\
               self.neutral +\
               self.aggressive +\
               self.offensive

    def mode(self):
        m = max((self.positive,
                 self.neutral,
                 self.aggressive,
                 self.offensive
                ))
        negative = self.offensive + self.aggressive

        # If empty
        if self.sum == 0: return "Neutral"
        # If the max is greater than negative, it must be positive or neutral
        elif (m > negative):
            if self.neutral == m: return "Neutral"
            elif self.positive == m: return "Positive"
        # If negative == positive it must be neutral
        elif (negative == self.positive): return "Neutral"
        # If aggressive or offensive is the highest it must be one of the 2
        elif self.aggressive == m and self.offensive == m: return "Aggressive & Offensive"
        elif self.aggressive == m: return "Aggressive"
        elif self.offensive == m: return "Offensive"

    def incrementPos(self):
        self.positive+=1
        self.save()

    def incrementNeut(self):
        self.neutral+=1
        self.save()

    def incrementOff(self):
        self.offensive+=1
        self.save()

    def incrementAgg(self):
        self.aggressive+=1
        self.save()

    def incrementBoth(self):
        self.offensive+=0.5
        self.aggressive+=0.5
        self.save()

    def normalise(self):
        # positive = 0
        # neutral = 0.5
        # negative = 1
        # therefore, aggressive + positive = 1

        #aggressive + offensive - neutral/2 - positive
        total = self.sum()
        return {"positive":self.positive/total, "neutral":self.neutral/total,
                "aggressive":self.aggressive/total, "offensive":self.offensive/total}

@receiver(post_save, sender=TweetResults)
def update(sender, instance, created, **kwargs):
    if instance.sum() >= 5:
        instance.valid = True
    else: 
        instance.valid = False
    post_save.disconnect(update, sender=TweetResults)
    instance.save()
    post_save.connect(update, sender=TweetResults)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    count = models.IntegerField(default=0) # tweets judged

    def __str__(self):
        return self.user.username
        
class UserTweetHistory(models.Model):

    class Judgement(models.TextChoices):
        POSITIVE   = "Positive"
        NEUTRAL    = "Neutral"
        OFFENSIVE  = "Offensive"
        AGGRESSIVE = "Aggressive"
        BOTH = "Both"
        SKIP = "Skipped"

    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    date  = models.DateField(default=datetime.date.today)
    judgement = models.CharField(
        max_length=20,
        choices=Judgement.choices,
        default=Judgement.NEUTRAL,
    )

