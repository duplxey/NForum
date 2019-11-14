from django import template
from django.contrib.auth.models import User

from accounts.models import Profile, Alert
from forum.models import Message, Thread

register = template.Library()


@register.filter(name='avatar')
def avatar(user):
    return Profile.get_profile(user).avatar.url


@register.filter(name='post_count')
def post_count(user):
    return Message.objects.filter(author=user).count()


@register.filter(name='thread_count')
def thread_count(user):
    return Thread.objects.filter(author=user).count()


@register.filter(name='upvote_count')
def upvote_count(user):
    return Profile.objects.get(user=user).get_upvotes()


@register.filter(name='downvote_count')
def downvote_count(user):
    return Profile.objects.get(user=user).get_downvotes()


@register.filter(name='unseen_alert_count')
def unseen_alert_count(user):
    return Alert.get_unseen_alerts(user).count()
