from django.shortcuts import render

from accounts.models import Profile
from .models import *


def index_view(request):
    return render(request, 'forum/index.html', {'categories': Category.objects.all(), 'recent_messages': Message.get_recent_messages(5), 'thread_count': Thread.get_thread_count(), 'message_count': Message.get_message_count(), 'registered_user_count': Profile.get_registered_user_count(), 'active_user_count': Profile.get_active_user_count()})


def thread_view(request, thread_title):
    if Thread.objects.filter(title=thread_title).exists():
        return render(request, 'forum/thread.html', {'thread': Thread.objects.get(title=thread_title)})
    else:
        return render(request, 'layout/message.html', {
            'message_type': "error",
            'message_title': "Unknown thread!",
            'message_content': "The requested thread could not be found."
        })


def subcategory_view(request, subcategory_name):
    if Subcategory.objects.filter(title=subcategory_name).exists():
        threads = Thread.objects.filter(subcategory=Subcategory.objects.get(title=subcategory_name))
        return render(request, 'forum/subcategory.html', {'subcategory': Subcategory.objects.get(title=subcategory_name), 'threads': threads})
    else:
        return render(request, 'layout/message.html', {
            'message_type': "error",
            'message_title': "Unknown subcategory!",
            'message_content': "This subcategory could not be found."
        })
