from typing import Any
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse

# Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Forms & Models
from user_web.forms import SignUpForm, ProfileForm
from user_web.models import Profile

# Messages
from django.contrib import messages

#other apps
from landing.views import homeview

def home(request):
    # Your logic for the home page
    return render(request, 'index.html')


def sign_up(request):
    form = SignUpForm()
    # registered = False

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            # registered = True
            messages.success(request, 'Account created successfully')
            return HttpResponseRedirect(reverse('login'))

    # dict = {'form':form, 'registered':registered}
    return render(request, 'signup.html', context={'form':form})


def login_user(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))

    return render(request,'login.html', context={'form':form})


@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, 'You have been logged out')
    return HttpResponseRedirect(reverse('home'))


@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            form = ProfileForm(instance=profile)

    return render(request, 'profile.html', context={'form':form})