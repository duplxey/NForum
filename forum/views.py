from django.shortcuts import render


def index(request):
    return render(request, 'forum/index.html', {})


def thread(request):
    return render(request, 'forum/thread.html', {})


def subcategory(request):
    return render(request, 'forum/subcategory.html', {})
