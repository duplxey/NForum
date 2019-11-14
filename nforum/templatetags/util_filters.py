from django import template

register = template.Library()


@register.filter(name='count_trues')
def count_trues(dictionary):
    i = 0
    for key in dictionary:
        if dictionary[key]:
            i = i + 1
    return i
