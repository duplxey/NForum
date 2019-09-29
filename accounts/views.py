from django.shortcuts import render


def login(request):
    return render(request, 'accounts/login.html', {})


def signup(request):
    return render(request, 'accounts/signup.html', {})


def logout(request):
    return render(request, 'accounts/logout.html', {})
