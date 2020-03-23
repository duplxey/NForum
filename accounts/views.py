from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, SignupForm, SettingsForm
from accounts.models import UserProfile, Alert, Achievement
from forum.models import Message, Thread
from nforum.errors import unknown_user, already_authenticated


def login_view(request):
    if request.user.is_authenticated:
        return already_authenticated(request)

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if not form.is_valid():
            return render(request, 'accounts/login.html', {'form': form})

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user is None:
            form.add_error('password', "Wrong username or password!")
            return render(request, 'accounts/login.html', {'form': form})

        login(request, user)
        return redirect('accounts-profile', username=request.user.username)
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})


def signup_view(request):
    if request.user.is_authenticated:
        return already_authenticated(request)

    if request.method == 'POST':

        form = SignupForm(request.POST)

        if not form.is_valid():
            return render(request, 'accounts/signup.html', {'form': form})

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

        login(request, user)

        return redirect('accounts-profile', username=request.user.username)
    else:
        form = SignupForm()
        return render(request, 'accounts/signup.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html', {})


def members_view(request):
    paginator = Paginator(User.objects.all(), 25)
    page = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'accounts/members.html', {
        'page': page,
    })


def profile_specific_view(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return unknown_user(request)

    recent_posts = Message.objects.filter(author=user).order_by("-date_posted")[:5]
    recent_threads = Thread.objects.filter(author=user)[::-1][:5]

    return render(request, 'accounts/profile.html', {
        'passed_user': user,
        'recent_posts': recent_posts,
        'recent_threads': recent_threads
    })


@login_required
def settings_view(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid():
            description = form.data.get('description', None)
            avatar = request.FILES.get('avatar', None)

            if description is not None:
                if description is not profile.description:
                    profile.description = description

            if avatar is not None:
                if avatar.size > 2097152:
                    form.add_error('avatar', "Image is too big! Max 2MB.")
                    return render(request, 'accounts/settings.html', {'form': form})

                if avatar is not profile.avatar:
                    profile.avatar = avatar

            profile.save()
        return redirect('accounts-profile', username=user.username)
    else:
        form = SettingsForm(initial={'description': profile.description, 'avatar': profile.avatar})
        return render(request, 'accounts/settings.html', {'form': form})


@login_required
def alert_view(request):
    Alert.clear_unseen_alerts(user=request.user)
    return render(request, 'accounts/alert.html', {'alerts': Alert.get_latest_alerts(request.user, 10)})


@login_required
def achievement_view(request):
    return render(request, 'accounts/achievement.html', {'unlocked_achievements': Achievement.get_unlocked_achievements(request.user), 'locked_achievements': Achievement.get_locked_achievements(request.user)})
