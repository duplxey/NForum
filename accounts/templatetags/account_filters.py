from django import template
from django.contrib.auth.models import User

from accounts.models import Profile

register = template.Library()


@register.filter(name='avatar')
def avatar(username):
    return Profile.objects.get(user=User.objects.get(username=username)).avatar.url
