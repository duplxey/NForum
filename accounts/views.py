from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render

from accounts.forms import LoginForm, SignupForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'accounts/home.html', {'form': form})
            else:
                return render(request, 'accounts/login.html', {'form': form})
        else:
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                form.add_error('confirm_password', "Passwords do not match!")
                return render(request, 'accounts/signup.html', {'form': form})

            if User.objects.filter(username=username).exists():
                form.add_error('username', "User with this username already exists.")
                return render(request, 'accounts/signup.html', {'form': form})

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            return render(request, 'accounts/signup.html', {'form': form})
        else:
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html', {})


def home(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/home.html', {})
    else:
        return render(request, 'home/index.html', {})


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/profile.html', {})
    else:
        return render(request, 'home/index.html', {})


def profile_specific(request, username):
    return render(request, 'layout/message.html', {
        'message_type': "error",
        'message_title': "User cannot be found.",
        'message_content': "This user does not exist!"
    })
