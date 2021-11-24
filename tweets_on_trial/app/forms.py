from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

inJudge = [0,1,2,3,4]

class TweetSubmission(forms.Form):

    inputJudgement = forms.CharField(label = "inputJudgement", widget=forms.HiddenInput(attrs={'id': 'inputJudgement', 'onchange':'submit()'}))

    isNegative = forms.BooleanField(label = "isNegative", widget=forms.HiddenInput(attrs={'id': 'isNegative', 'onchange':'submit()'}))
