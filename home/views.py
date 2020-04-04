from django.contrib.auth.models import User
from django.shortcuts import render

from forum.models import ForumConfiguration, Thread, Message


def home_view(request):
    forum_config = ForumConfiguration.get_solo()

    threads = []
    if forum_config.home_category:
        threads = reversed(Thread.objects.filter(subcategory__category=forum_config.home_category))

    return render(request, 'forum/home.html', {
        'threads': threads,
        'recent_messages': Message.get_recent_messages(5),
        'thread_count': Thread.objects.count(),
        'message_count': Message.objects.count(),
        'registered_user_count': User.objects.count(),
        'active_user_count': User.objects.filter(is_active=True).count(),
    })