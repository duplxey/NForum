from django.contrib.auth.models import User
from django.shortcuts import render

from forum.models import Thread, Message
from nforum.errors import search_failed


def search_view(request):
    query = request.GET.get('query')

    if query is None or len(query) < 2 or len(query) > 16:
        return search_failed(request)

    related_threads = Thread.objects.filter(title__icontains=query)
    related_users = User.objects.filter(username__icontains=query)
    related_messages = Message.objects.filter(content__icontains=query)

    return render(request, 'search/search.html', {'keyword': query, 'related_threads': related_threads, 'related_messages': related_messages, 'related_users': related_users})

