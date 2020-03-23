from django.contrib.auth.models import User
from django.shortcuts import render

from forum.models import Thread, Message
from nforum.errors import search_failed


def search_view(request):
    query = request.GET.get('query')

    if query is None or len(query) < 2 or len(query) > 16:
        return search_failed(request)

    return render(request, 'search/search.html', {
        'keyword': query,
        'related_threads': Thread.objects.filter(title__icontains=query),
        'related_messages': Message.objects.filter(content__icontains=query),
        'related_users': User.objects.filter(username__icontains=query)
    })

