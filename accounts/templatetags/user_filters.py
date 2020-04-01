from django import template

from accounts.models import UserProfile, Alert
from forum.models import Message, Thread

register = template.Library()


@register.filter(name='avatar')
def avatar(user):
    return "UserProfile.get_profile(user).avatar.url"


@register.filter(name='post_count')
def post_count(user):
    return Message.objects.filter(author=user).count()


@register.filter(name='thread_count')
def thread_count(user):
    return Thread.objects.filter(author=user).count()


@register.filter(name='upvote_count')
def upvote_count(user):
    return UserProfile.get_profile(user=user).get_upvotes()


@register.filter(name='downvote_count')
def downvote_count(user):
    return UserProfile.get_profile(user=user).get_downvotes()


@register.filter(name='reputation')
def reputation(user):
    return UserProfile.get_profile(user=user).get_reputation()


@register.filter(name='achievements')
def achievements(user):
    return UserProfile.get_profile(user=user).get_achievements()


@register.filter(name='unseen_alert_count')
def unseen_alert_count(user):
    return Alert.get_unseen_alerts(user).count()
