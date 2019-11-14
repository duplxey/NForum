from django import template
from django.contrib.auth.models import User

from accounts.models import Profile, Alert
from forum.models import Message, Thread

register = template.Library()


@register.filter(name='avatar')
def avatar(username):
    return Profile.objects.get(user=User.objects.get(username=username)).avatar.url


@register.filter(name='post_count')
def post_count(username):
    return Message.objects.filter(author=User.objects.get(username=username)).count()


@register.filter(name='thread_count')
def thread_count(username):
    return Thread.objects.filter(author=User.objects.get(username=username)).count()


@register.filter(name='upvote_count')
def profile(username):
    return Profile.objects.get(user=User.objects.get(username=username)).get_upvotes()


@register.filter(name='downvote_count')
def profile(username):
    return Profile.objects.get(user=User.objects.get(username=username)).get_downvotes()


@register.filter(name='unseen_alert_count')
def unseen_alert_count(user):
    return Alert.get_unseen_alerts(user).count()
