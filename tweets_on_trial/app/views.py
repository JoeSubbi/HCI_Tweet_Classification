from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from app.models import Tweet, TweetResults

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {'boldmessage': 'ANALYTICS'}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'app/index.html', context=context_dict)

def judge(request):
    context_dict = {}
    obj, created = Tweet.objects.get_or_create(body = "Can't wait to get battered into this chippy")
    context_dict['tweet'] = obj

    if request.is_ajax:


        isNegative = request.POST.get('isNegative')
        inputJudgement = request.POST.get('inputJudgement')

        print(isNegative)

    return render(request, 'app/judgement.html', context=context_dict)

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

