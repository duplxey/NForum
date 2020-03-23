from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

import math

from django.utils import timezone
from django.views.decorators.http import require_http_methods

from accounts.models import UserProfile, Alert, Achievement
from forum.forms import CreateThreadForm, PostReplyForm, PostDeleteForm
from nforum.errors import insufficient_permission, unknown_thread, unknown_subcategory, unknown_message
from .models import *


def index_view(request):
    return render(request, 'forum/index.html', {
        'categories': Category.objects.all(),
        'recent_messages': Message.get_recent_messages(5),
        'thread_count': Thread.objects.count(),
        'message_count': Message.objects.count(),
        'registered_user_count': UserProfile.get_registered_user_count(),
        'active_user_count': UserProfile.get_active_user_count()
    })


def thread_view(request, thread_title):
    try:
        thread = Thread.objects.get(title=thread_title)
    except Thread.DoesNotExist:
        return unknown_thread(request)

    return render(request, 'forum/thread.html', {
        'thread': thread,
        'form': PostReplyForm()
    })


@login_required
def thread_create_view(request, subcategory_name):
    try:
        subcategory = Subcategory.objects.get(title=subcategory_name)
    except Subcategory.DoesNotExist:
        return unknown_subcategory(request)

    form = CreateThreadForm()

    if request.method == 'POST':
        form = CreateThreadForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            prefix = form.cleaned_data['prefix']

            if Thread.objects.filter(title=title).exists():
                form.add_error('title', "Thread with this name already exists.")
                return render(request, 'forum/thread-create.html', {'form': form, 'subcategory': subcategory})

            if prefix is not None:
                if not ThreadPrefix.objects.filter(name=prefix).exists():
                    form.add_error('prefix', "Unknown thread prefix.")
                    return render(request, 'forum/thread-create.html', {'form': form, 'subcategory': subcategory})

            thread = Thread.objects.create(title=title, author=request.user, subcategory=subcategory, prefix=prefix)
            thread.save()

            message = Message.objects.create(thread=thread, content=content, author=request.user)
            message.save()

            return redirect(thread_view, thread_title=thread.title)

    return render(request, 'forum/thread-create.html', {
        'form': form,
        'subcategory': subcategory
    })


@login_required
def thread_post_view(request, thread_title):
    try:
        thread = Thread.objects.get(title=thread_title)
    except Thread.DoesNotExist:
        return unknown_thread(request)

    form = PostReplyForm()

    if request.method == 'POST':
        form = PostReplyForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']

            message = Message.objects.create(thread=thread, content=content, author=request.user)
            message.save()

            # Send an alert to all the participants
            for participant in thread.get_participants():
                if participant == request.user:
                    continue
                alert = Alert(user=participant, type=Alert.RESPOND, caused_by=request.user, thread=thread)
                alert.save()

            return redirect(thread_view, thread_title=thread.title)

    return render(request, 'forum/thread.html', {
        'form': form,
        'thread': thread,
    })


@login_required
def message_edit_view(request, message_id):
    try:
        message = Message.objects.get(pk=message_id)
    except Message.DoesNotExist:
        return unknown_message(request)
    thread = message.thread

    if not message.author == request.user:
        return insufficient_permission(request)

    form = PostReplyForm(initial={'content': message.content})

    if request.method == 'POST':
        form = PostReplyForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']

            message.content = content
            message.date_edited = timezone.now()
            message.save()

            return redirect(thread_view, thread_title=thread.title)

    return render(request, 'forum/message-edit.html', {
        'form': form,
        'thread': thread,
        'message': message
    })


@login_required
def message_remove_view(request, message_id):
    try:
        message = Message.objects.get(pk=message_id)
    except Message.DoesNotExist:
        return unknown_message(request)
    thread = message.thread

    if not message.author == request.user:
        return insufficient_permission(request)

    form = PostDeleteForm()

    if request.method == 'POST':
        form = PostDeleteForm(request.POST)

        if form.is_valid():
            if thread.get_first_message() == message:
                thread.delete()
                return redirect('forum-index')
            else:
                message.delete()
                return redirect('forum-thread', thread_title=thread.title)

    return render(request, 'forum/message-delete.html', {
        'form': form,
        'thread': thread,
        'message': message
    })


# TODO: achievement signals

@login_required
@require_http_methods(["POST"])
def message_rate(request):
    pk = request.POST.get("pk", None)

    try:
        message = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return HttpResponseBadRequest("Invalid message.")

    if message.author == request.user:
        return HttpResponseBadRequest("You can't rate your own posts.")

    try:
        value = int(request.POST.get("value", None))
    except ValueError:
        return HttpResponseBadRequest("Value cannot be parsed to an integer.")

    if value > 0:
        message.upvote(request.user)
        Achievement.check_add_achievements(message.author, Achievement.UPVOTE_COUNT)
    else:
        message.downvote(request.user)
        Achievement.check_add_achievements(message.author, Achievement.DOWNVOTE_COUNT)

    return JsonResponse({
        'pk': message.pk,
        'upvoters': message.upvoters.count(),
        'downvoters': message.downvoters.count(),
    })


def subcategory_view(request, subcategory_name):
    try:
        subcategory = Subcategory.objects.get(title=subcategory_name)
    except Subcategory.DoesNotExist:
        return unknown_subcategory(request)

    return subcategory_page_view(request=request, subcategory_name=subcategory.title, page=0)


def subcategory_page_view(request, subcategory_name, page):
    try:
        subcategory = Subcategory.objects.get(title=subcategory_name)
    except Subcategory.DoesNotExist:
        return unknown_subcategory(request)

    threads_per_page = 12
    subcategory_threads = Thread.objects.filter(subcategory=subcategory).order_by('-pk')
    threads = subcategory_threads[page*threads_per_page:(page+1)*threads_per_page]

    previous_page = page - 1
    if previous_page < 0:
        previous_page = None

    next_page = page + 1
    if next_page > math.ceil(subcategory_threads.count()/threads_per_page) - 1:
        next_page = None

    return render(request, 'forum/subcategory.html', {
        'subcategory': subcategory,
        'threads': threads,
        'page': page,
        'previous_page': previous_page,
        'next_page': next_page,
        'thread_per_page': threads_per_page
    })
