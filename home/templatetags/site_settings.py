from django import template

from home.models import SiteSocialNetwork

register = template.Library()


@register.simple_tag(name='social_networks')
def social_networks():
    return SiteSocialNetwork.objects.all()
