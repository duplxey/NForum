from django import template
from django.template.defaultfilters import safe

from forum.models import Message, Thread
from members.models import Alert
from settings.models import SiteColorPalette

register = template.Library()


@register.filter(name='avatar')
def avatar(user):
    if user.userprofile.avatar:
        return user.userprofile.avatar.url
    else:
        special_color = SiteColorPalette.objects.get().special_color
        text_color_light = SiteColorPalette.objects.get().text_color_light
        return "https://eu.ui-avatars.com/api/?background=" + special_color + "&color=" + text_color_light + "&bold=true&name=" + user.username + "&size=200"


@register.filter(name='post_count')
def post_count(user):
    return Message.objects.filter(author=user).count()


@register.filter(name='thread_count')
def thread_count(user):
    return Thread.objects.filter(author=user).count()


@register.filter(name='upvote_count')
def upvote_count(user):
    return user.userprofile.get_upvotes()


@register.filter(name='downvote_count')
def downvote_count(user):
    return user.userprofile.get_downvotes()


@register.filter(name='reputation')
def reputation(user):
    return user.userprofile.get_reputation()


@register.filter(name='formatted_reputation')
def formatted_reputation(user):
    user_reputation = user.userprofile.get_reputation()
    if user_reputation > 0:
        return safe("<span class='text-success'>" + str(user_reputation) + "</span>")
    elif user_reputation < 0:
        return safe("<span class='text-danger'>" + str(user_reputation) + "</span>")
    else:
        return safe("<span class='text-warning'>0</span>")


@register.filter(name='achievements')
def achievements(user):
    return user.userprofile.get_achievements()


@register.filter(name='unseen_alert_count')
def unseen_alert_count(user):
    return Alert.get_unseen_alerts(user).count()
