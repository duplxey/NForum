from django.shortcuts import render, redirect

from accounts.models import Profile, Alert, Achievement
from forum.forms import CreateThreadForm, PostReplyForm, PostDeleteForm
from nforum.errors import insufficient_permission, unknown_thread, unknown_subcategory, unknown_message, \
    not_authenticated
from .models import *


def index_view(request):
    return render(request, 'forum/index.html', {
        'categories': Category.objects.all(),
        'recent_messages': Message.get_recent_messages(5),
        'thread_count': Thread.get_thread_count(),
        'message_count': Message.get_message_count(),
        'registered_user_count': Profile.get_registered_user_count(),
        'active_user_count': Profile.get_active_user_count()
    })


def thread_view(request, thread_title):
    if not Thread.objects.filter(title=thread_title).exists():
        return unknown_thread(request)

    return render(request, 'forum/thread.html', {'thread': Thread.objects.get(title=thread_title), 'form': PostReplyForm()})


def thread_create_view(request, subcategory_name):
    if not Subcategory.objects.filter(title=subcategory_name).exists():
        return unknown_subcategory(request)

    if request.method == 'POST':
        form = CreateThreadForm(request.POST)

        if not form.is_valid():
            return render(request, 'forum/thread-create.html', {'form': form, 'subcategory': Subcategory.objects.get(title=subcategory_name)})

        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        prefix = form.cleaned_data['prefix']

        if Thread.objects.filter(title=title).exists():
            form.add_error('title', "Thread with this name already exists.")
            return render(request, 'forum/thread-create.html', {'form': form, 'subcategory': Subcategory.objects.get(title=subcategory_name)})

        if prefix is not None:
            if not ThreadPrefix.objects.filter(name=prefix).exists():
                form.add_error('prefix', "Unknown thread prefix.")
                return render(request, 'forum/thread-create.html', {'form': form, 'subcategory': Subcategory.objects.get(title=subcategory_name)})

        thread = Thread.objects.create(title=title, author=request.user, subcategory=Subcategory.objects.get(title=subcategory_name), prefix=prefix)
        thread.save()

        message = Message.objects.create(thread=thread, content=content, author=request.user)
        message.save()

        # Let's check if user achieved anything
        Achievement.check_add_achievements(request.user, Achievement.THREAD_COUNT)

        return redirect(thread_view, thread_title=thread.title)
    else:
        form = CreateThreadForm()
    return render(request, 'forum/thread-create.html', {'form': form, 'subcategory': Subcategory.objects.get(title=subcategory_name)})


def thread_post_view(request, thread_title):
    if not Thread.objects.filter(title=thread_title).exists():
        return unknown_thread(request)

    thread = Thread.objects.get(title=thread_title)

    if request.method == 'POST':
        form = PostReplyForm(request.POST)

        if not form.is_valid():
            form = PostReplyForm()
            return render(request, 'forum/thread.html', {'form': form, 'thread': Thread.objects.get(title=thread_title)})

        content = form.cleaned_data['content']

        message = Message.objects.create(thread=thread, content=content, author=request.user)
        message.save()

        # Send an alert to all the participants
        for participant in thread.get_participants():
            if participant == request.user:
                continue
            alert = Alert(user=participant, type=Alert.RESPOND, caused_by=request.user, thread=thread)
            alert.save()

        # Let's check if user achieved anything
        Achievement.check_add_achievements(request.user, Achievement.POST_COUNT)

        return redirect(thread_view, thread_title=thread.title)
    else:
        form = PostReplyForm()
        return render(request, 'forum/thread.html', {'form': form, 'thread': Thread.objects.get(title=thread_title)})


def message_edit_view(request, message_id):
    if not Message.objects.filter(pk=message_id).exists():
        return unknown_message(request)

    message = Message.objects.get(pk=message_id)
    thread = message.thread

    if not message.author == request.user:
        return insufficient_permission(request)

    if request.method == 'POST':
        form = PostReplyForm(request.POST)

        if not form.is_valid():
            form = PostReplyForm(initial={'content': message.content})
            return render(request, 'forum/message-edit.html', {'form': form, 'thread': Thread.objects.get(title=thread.title), 'message': message})

        content = form.cleaned_data['content']

        message.content = content
        message.save()

        return redirect(thread_view, thread_title=thread.title)
    else:
        form = PostReplyForm(initial={'content': message.content})
        return render(request, 'forum/message-edit.html', {'form': form, 'thread': Thread.objects.get(title=thread.title), 'message': message})


def message_remove_view(request, message_id):
    if not Message.objects.filter(pk=message_id).exists():
        return unknown_message(request)

    message = Message.objects.get(pk=message_id)
    thread = message.thread

    if not message.author == request.user:
        return insufficient_permission(request)

    if request.method == 'POST':
        form = PostDeleteForm(request.POST)

        if not form.is_valid():
            return render(request, 'forum/message-delete.html', {'form': PostDeleteForm(), 'thread': thread, 'message': message})

        if thread.get_first_message() == message:
            thread.delete()
            return redirect('forum-index')
        else:
            message.delete()
            return redirect('forum-thread', thread_title=thread.title)
    else:
        return render(request, 'forum/message-delete.html', {'form': PostDeleteForm(), 'thread': thread, 'message': message})


def message_upvote(request, message_id):
    if not Message.objects.filter(pk=message_id).exists():
        return unknown_message(request)

    if not request.user.is_authenticated:
        return not_authenticated(request)

    message = Message.objects.get(pk=message_id)
    thread = message.thread

    if message.author == request.user:
        return redirect(thread_view, thread_title=thread.title)

    if request.user in message.upvoters.all():
        message.upvoters.remove(request.user)
        return redirect(thread_view, thread_title=thread.title)

    message.upvoters.add(request.user)

    # Send an alert to the author
    alert = Alert(user=message.author, type=Alert.UPVOTE, caused_by=request.user, thread=thread)
    alert.save()

    # Let's check if the author achieved anything
    Achievement.check_add_achievements(message.author, Achievement.UPVOTE_COUNT)

    if request.user in message.downvoters.all():
        message.downvoters.remove(request.user)

    return redirect(thread_view, thread_title=thread.title)


def message_downvote(request, message_id):
    if not Message.objects.filter(pk=message_id).exists():
        return unknown_message(request)

    if not request.user.is_authenticated:
        return not_authenticated(request)

    message = Message.objects.get(pk=message_id)
    thread = message.thread

    if message.author == request.user:
        return redirect(thread_view, thread_title=thread.title)

    if request.user in message.downvoters.all():
        message.downvoters.remove(request.user)
        return redirect(thread_view, thread_title=thread.title)

    message.downvoters.add(request.user)

    # Send an alert to the author
    alert = Alert(user=message.author, type=Alert.DOWNVOTE, caused_by=request.user, thread=thread)
    alert.save()

    # Let's check if the author achieved anything
    Achievement.check_add_achievements(message.author, Achievement.DOWNVOTE_COUNT)

    if request.user in message.upvoters.all():
        message.upvoters.remove(request.user)

    return redirect(thread_view, thread_title=thread.title)


def subcategory_view(request, subcategory_name):
    if not Subcategory.objects.filter(title=subcategory_name).exists():
        return unknown_subcategory(request)

    threads = Thread.objects.filter(subcategory=Subcategory.objects.get(title=subcategory_name))
    return render(request, 'forum/subcategory.html', {'subcategory': Subcategory.objects.get(title=subcategory_name), 'threads': threads})
