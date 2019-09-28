from django.shortcuts import render


def index(request):
    return render(request, 'forum/index.html', {})


def thread(request):
    return render(request, 'forum/thread.html', {})
