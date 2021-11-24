from django.shortcuts import render
from django.http import HttpResponse
from .forms import TweetSubmission

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {'boldmessage': 'ANALYTICS'}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'app/index.html', context=context_dict)

def judge(request):
    context_dict = {'boldmessage': 'ANALYTICS'}

    if request.is_ajax:


        isNegative = request.POST.get('isNegative')
        inputJudgement = request.POST.get('inputJudgement')

        print(isNegative)

    return  render(request, 'app/judgement.html', context=context_dict)
