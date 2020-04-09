from django import template
from django.template.defaultfilters import safe

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


@register.filter(name='reputation')
def reputation(user):
    rep = user.userprofile.get_reputation()
    if rep > 0:
        return safe("<span class='text-success'>" + str(rep) + "</span>")
    elif rep < 0:
        return safe("<span class='text-danger'>" + str(rep) + "</span>")
    else:
        return safe("<span class='text-warning'>0</span>")
