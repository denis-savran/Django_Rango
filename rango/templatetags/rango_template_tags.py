from django import template
from django.shortcuts import reverse

from ..models import Category

register = template.Library()


@register.inclusion_tag('rango/cats.html')
def get_category_list(active_category=None):
    return {'cats': Category.objects.all(), 'act_cat': active_category}


@register.inclusion_tag('rango/nav_item.html')
def dynamic_nav_item(current_url_name, url_name, a_tag_text, *args):
    if args:
        args = (arg for arg in args)
        url = reverse(url_name, args=args)
    else:
        url = reverse(url_name)

    context_dict = {'url': url, 'a_tag_text': a_tag_text, 'active': True}

    if current_url_name == url_name:
        context_dict['active'] = True
    else:
        context_dict['active'] = False

    return context_dict
