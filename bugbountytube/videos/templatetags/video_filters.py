from django import template

register = template.Library()

@register.filter(name='embed_url')
def embed_url(value):
    if "watch?v=" in value:
        return value.replace("watch?v=", "embed/")
    elif "youtu.be/" in value:
        return value.replace("youtu.be/", "youtube.com/embed/")
    return value
