from django.http import HttpResponse
from django.shortcuts import render

from accounts.forms import LoginForm

#
# def login(request):
#     return render(request, 'accounts/login.html', {})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return HttpResponse("yay")
        else:
            return HttpResponse("nay")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def signup(request):
    return render(request, 'accounts/signup.html', {})


def logout(request):
    return render(request, 'accounts/logout.html', {})
