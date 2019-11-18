from django.contrib.auth.models import User
from django.shortcuts import render

from forum.models import Thread
from nforum.errors import search_failed


def search_fail_view(request):
    return search_failed(request)


def search_view(request, keyword):
    related_threads = Thread.objects.filter(title__icontains=keyword)
    related_users = User.objects.filter(username__icontains=keyword)

    return render(request, 'search/search.html', {'keyword': keyword, 'related_threads': related_threads, 'related_users': related_users})
