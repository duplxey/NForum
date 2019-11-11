from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from accounts.models import Profile
from forum.forms import CreateThreadForm, PostReplyForm, PostDeleteForm
from nforum.errors import insufficient_permission
from .models import *


def index_view(request):
    return render(request, 'forum/index.html', {'categories': Category.objects.all(), 'recent_messages': Message.get_recent_messages(5), 'thread_count': Thread.get_thread_count(), 'message_count': Message.get_message_count(), 'registered_user_count': Profile.get_registered_user_count(), 'active_user_count': Profile.get_active_user_count()})


def thread_view(request, thread_title):
    if Thread.objects.filter(title=thread_title).exists():
        return render(request, 'forum/thread.html', {'thread': Thread.objects.get(title=thread_title), 'form': PostReplyForm()})
    else:
        return render(request, 'layout/message.html', {
            'message_type': "error",
            'message_title': "Unknown thread!",
            'message_content': "The requested thread could not be found."
        })


def thread_create_view(request, subcategory_name):
    if Subcategory.objects.filter(title=subcategory_name).exists():
        if request.method == 'POST':
            form = CreateThreadForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']

                if Thread.objects.filter(title=title).exists():
                    form.add_error('title', "Thread with this name already exists.")
                    return render(request, 'forum/thread-create.html', {'form': form, 'subcategory': Subcategory.objects.get(title=subcategory_name)})

                thread = Thread.objects.create(title=title, author=request.user, subcategory=Subcategory.objects.get(title=subcategory_name))
                thread.save()

                message = Message.objects.create(thread=thread, content=content, author=request.user)
                message.save()

                return render(request, 'forum/thread.html', {'thread': Thread.objects.get(title=thread.title)})
            else:
                return render(request, 'forum/thread-create.html', {'form': form, 'subcategory': Subcategory.objects.get(title=subcategory_name)})
        else:
            form = CreateThreadForm()
        return render(request, 'forum/thread-create.html', {'form': form, 'subcategory': Subcategory.objects.get(title=subcategory_name)})
    else:
        return render(request, 'layout/message.html', {
            'message_type': "error",
            'message_title': "Unknown subcategory!",
            'message_content': "This subcategory could not be found."
        })


def thread_post_view(request, thread_title):
    if Thread.objects.filter(title=thread_title).exists():
        thread = Thread.objects.get(title=thread_title)
        if request.method == 'POST':
            form = PostReplyForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']

                message = Message.objects.create(thread=thread, content=content, author=request.user)
                message.save()

                return HttpResponseRedirect(thread_title)
            else:
                form = PostReplyForm()
                return render(request, 'forum/thread.html', {'form': form, 'thread': Thread.objects.get(title=thread_title)})
        else:
            form = PostReplyForm()
            return render(request, 'forum/thread.html', {'form': form, 'thread': Thread.objects.get(title=thread_title)})
    else:
        return render(request, 'layout/message.html', {
            'message_type': "error",
            'message_title': "Unknown thread!",
            'message_content': "This thread could not be found."
        })


def message_edit_view(request, message_id):
    if Message.objects.filter(pk=message_id).exists():
        message = Message.objects.get(pk=message_id)

        if not message.author == request.user:
            return insufficient_permission(request)

        thread_title = message.thread.title
        if request.method == 'POST':
            form = PostReplyForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']

                message.content = content
                message.save()

                return render(request, 'forum/thread.html', {'form': form, 'thread': Thread.objects.get(title=thread_title)})
            else:
                form = PostReplyForm(initial={'content': message.content})
                return render(request, 'forum/message-edit.html', {'form': form, 'thread': Thread.objects.get(title=thread_title), 'message': message})
        else:
            form = PostReplyForm(initial={'content': message.content})
            return render(request, 'forum/message-edit.html', {'form': form, 'thread': Thread.objects.get(title=thread_title), 'message': message})
    else:
        return render(request, 'layout/message.html', {
            'message_type': "error",
            'message_title': "Unknown message!",
            'message_content': "This message could not be found."
        })


def message_remove_view(request, message_id):
    message = Message.objects.get(pk=message_id)
    thread = message.thread

    if not message.author == request.user:
        return insufficient_permission(request)

    if request.method == 'POST':
        form = PostDeleteForm(request.POST)

        if form.is_valid():

            if thread.get_first_message() == message:
                thread.delete()
                return redirect('forum-index')
            else:
                message.delete()
                return redirect('forum-thread', thread_title=thread.title)
        else:
            return render(request, 'forum/message-delete.html', {'form': PostDeleteForm(), 'thread': thread, 'message': message})
    else:
        return render(request, 'forum/message-delete.html', {'form': PostDeleteForm(), 'thread': thread, 'message': message})


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
