import json

from django import template

register = template.Library()


@register.filter
def to_heading(value):
    value = value.replace("_", " ")
    value = value.capitalize()
    return value

@register.filter
def to_url(value):
    if value is not None:
        value = value.replace("\\","/")
    return value

