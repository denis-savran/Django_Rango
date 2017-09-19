import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_Rango.settings')

import django

django.setup()
from rango.models import Category, Page


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def populate():
    python_pages = [
        {"title": "Official Python Tutorial",
         "url": "http://docs.python.org/2/tutorial/",
         "views": 1200},
        {"title": "How to Think like a Computer Scientist",
         "url": "http://www.greenteapress.com/thinkpython/",
         "views": 235},
        {"title": "Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/",
         "views": 282}]

    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "https://docs.djangoproject.com/en/1.11/intro/tutorial01/",
         "views": 589},
        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com/",
         "views": 560},
        {"title": "How to Tango with Django",
         "url": "http://www.tangowithdjango.com/",
         "views": 811}]

    other_pages = [
        {"title": "Bottle",
         "url": "http://bottlepy.org/docs/dev/",
         "views": 358},
        {"title": "Flask",
         "url": "http://flask.pocoo.org",
         "views": 260}]

    cats = {"Python": {"views": 128, "likes": 64, "pages": python_pages},
            "Django": {"views": 64, "likes": 32, "pages": django_pages},
            "Other Frameworks": {"views": 32, "likes": 16, "pages": other_pages}}

    for cat, cat_data in cats.items():
        c = add_cat(name=cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(cat=c, title=p['title'], url=p['url'], views=p['views'])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print('- {0} - {1}'.format(str(c), str(p)))


if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
