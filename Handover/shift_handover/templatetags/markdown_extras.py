from markdown import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text: str):
    #Now we're vulnerable for XSS
    return mark_safe(markdown(text))