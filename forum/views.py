import re

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from members.models import Achievement, Alert
from forum.forms import CreateThreadForm, PostReplyForm, PostDeleteForm
from nforum.errors import insufficient_permission, unknown_thread, unknown_subcategory, unknown_message
from .models import *


def home_view(request):
    forum_config = ForumConfiguration.get_solo()

    page = []
    if forum_config.index_category:
        paginator = Paginator(Thread.objects.filter(subcategory__category=forum_config.index_category), 5)
        page = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'forum/home.html', {
        'category': forum_config.index_category,
        'page': page,
        'recent_messages': Message.get_recent_messages(5),
        'thread_count': Thread.objects.count(),
        'message_count': Message.objects.count(),
        'registered_user_count': User.objects.count(),
        'active_user_count': User.objects.filter(is_active=True).count(),
    })


def forum_view(request):
    return render(request, 'forum/index.html', {
        'categories': Category.objects.all(),
        'recent_messages': Message.get_recent_messages(5),
        'thread_count': Thread.objects.count(),
        'message_count': Message.objects.count(),
        'registered_user_count': User.objects.count(),
        'active_user_count': User.objects.filter(is_active=True).count(),
    })


def thread_view(request, thread_title):
    try:
        thread = Thread.objects.get(title=thread_title)
    except Thread.DoesNotExist:
        return unknown_thread(request)

    paginator = Paginator(thread.get_messages(), 10)
    page = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'forum/thread.html', {
        'thread': thread,
        'page': page,
        'form': PostReplyForm()
    })


@login_required
def thread_create_view(request, subcategory_name):
    try:
        subcategory = Subcategory.objects.get(title=subcategory_name)
    except Subcategory.DoesNotExist:
        return unknown_subcategory(request)

    if subcategory.category.staff_only and not request.user.has_perm("create_thread_in_staff_only"):
        return insufficient_permission(request)

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

            message.author.userprofile.check_add_achievements(Achievement.THREAD_COUNT)

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

    if thread.locked and not request.user.has_perm("locked_thread_reply"):
        return insufficient_permission(request)

    form = PostReplyForm()

    if request.method == 'POST':
        form = PostReplyForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']

            message = Message.objects.create(thread=thread, content=content, author=request.user)
            message.save()

            mentioned = []

            # Loop thru all the words and check if any user is mentioned
            pattern = re.compile("@[A-z0-9_]+")
            for match in pattern.findall(message.content):
                try:
                    user = User.objects.get(username=match.replace("@", ""))
                    Alert.objects.create(user=user, type=Alert.MENTION, caused_by=request.user, thread=thread)
                    mentioned.append(user)
                except User.DoesNotExist:
                    continue

            # Send an alert to all the participants (if already mentioned skip)
            for participant in thread.get_participants():
                if participant == request.user or participant in mentioned:
                    continue
                Alert.objects.create(user=participant, type=Alert.RESPOND, caused_by=request.user, thread=thread)

            message.author.userprofile.check_add_achievements(Achievement.POST_COUNT)

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
        message.author.userprofile.check_add_achievements(Achievement.UPVOTE_COUNT)
        Alert.objects.create(user=message.author, type=Alert.UPVOTE, caused_by=request.user, thread=message.thread)
    else:
        message.downvote(request.user)
        message.author.userprofile.check_add_achievements(Achievement.DOWNVOTE_COUNT)
        Alert.objects.create(user=message.author, type=Alert.DOWNVOTE, caused_by=request.user, thread=message.thread)

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

    paginator = Paginator(Thread.objects.filter(subcategory=subcategory).order_by("-pinned"), 12)
    page = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'forum/subcategory.html', {
        'subcategory': subcategory,
        'page': page,
    })
