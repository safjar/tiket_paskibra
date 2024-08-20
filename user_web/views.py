from typing import Any
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse

# Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Forms & Models
from user_web.forms import SignUpForm, ProfileForm
from user_web.models import Profile

# Messages
from django.contrib import messages

#other apps
from landing.views import homeview
from bayar.views import panitia


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
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            print(f"Email: {email}, Password: {password}")  # Debugging

            user = authenticate(username=email, password=password)

            if user is not None:
                print(f"Authenticated user: {user}")  # Debugging
                login(request, user)
                if user.is_staff:
                    return HttpResponseRedirect(reverse('panitia'))
                else:
                    return HttpResponseRedirect(reverse('home'))
            else:
                print("Authentication failed")  # Debugging

    return render(request, 'login.html', context={'form': form})

@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, 'You have been logged out')
    return HttpResponseRedirect(reverse('home'))


@login_required
def user_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Jika profil tidak ada, buat objek profil baru
        profile = Profile(user=request.user)
    
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')  # Redirect untuk menghindari resubmit form
        
        

    return render(request, 'profile.html', context={'form': form})

