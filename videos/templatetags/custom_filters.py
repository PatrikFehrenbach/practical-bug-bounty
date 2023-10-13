from django import template
import json

register = template.Library()

@register.filter(name='get_icon')
def get_icon(icons_dict, key):
    return icons_dict.get(key, '')

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='json_parse')
def json_parse(value):
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return {}