from django import template
from rango.models import Category

register = template.Library()


@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(), 'act_cat': cat}


@register.inclusion_tag('rango/nav_item.html')
def dynamic_nav_item(current_url_name, url_name, a_tag_text):
    if current_url_name == url_name:
        return {'url_name': url_name, 'a_tag_text': a_tag_text, 'active': True}
    else:
        return {'url_name': url_name, 'a_tag_text': a_tag_text, 'active': False}
