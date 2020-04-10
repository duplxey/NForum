from django import template
from django.template.defaultfilters import safe

register = template.Library()


@register.filter(name='with_prefix')
def with_prefix(thread):
    if thread.prefix:
        return safe(
            "<span class='badge' style='background: #" + thread.prefix.color + "; color:white;'>" + thread.prefix.name + "</span> " + thread.title
        )
    else:
        return safe(thread.title)
