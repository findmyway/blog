import re

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter(name='remove_all_img')
@stringfilter
def remove_all_img(value):
    """Removes all img links from the given string"""
    return re.sub(r'<img .+?>', '', value)


@register.filter(name='extract_first_img')
@stringfilter
def extract_first_img(value):
    """extract first img links from the given string"""
    search_result = re.search(r'(<img .+?>)', value)
    if search_result:
        return search_result.group()
    else:
        return ""

