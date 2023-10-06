from django import template

register = template.Library()

@register.filter(name='embed_url')
def embed_url(value):
    return value.replace("watch?v=", "embed/")
