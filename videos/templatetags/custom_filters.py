from django import template

register = template.Library()

@register.filter(name='get_icon')
def get_icon(icons_dict, key):
    return icons_dict.get(key, '')
