from django.db import models

class Tweet(models.Model):
    body = models.CharField(max_length=256)

    def __str__(self):
        return self.body

class TweetResults(models.Model):
    
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    positive  = models.IntegerField(default=0)
    neutral   = models.IntegerField(default=0)
    agressive = models.IntegerField(default=0)
    offensive = models.IntegerField(default=0)

    def __str__(self):
        return f"\tPositive:  {self.positive}\n"\
               f"\tNeutral:   {self.neutral}\n"\
               f"\tAgressive: {self.agressive}\n"\
               f"\tOffensive: {self.offensive}"

    class Meta:
        verbose_name_plural = 'Tweet Results'

    def sum(self):
        return self.positive +\
               self.neutral +\
               self.agressive +\
               self.offensive

    def mode(self):
        return max((self.positive,
                    self.neutral,
                    self.aggressive,
                    self.offensive
                   ))

    def normalise(self):
        # positive = 0
        # neutral = 0.5
        # negative = 1
        # therefore, aggressive + positive = 1

        #agressive + offensive - neutral/2 - positive
        ratio = (self.agressive + self.offensive)/2 -\
                 self.neutral/2 - self.positive
        return (self.positive/ratio, self.neutral/ratio,
                self.agressive/ratio, self.offensive/ratio)

