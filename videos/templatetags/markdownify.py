from django import template
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

register = template.Library()

@register.filter
def formatted_markdown(text):
    return mark_safe(markdownify(text))
