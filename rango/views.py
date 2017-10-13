from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page, UserProfile
from rango.utils import visitor_cookie_handler


def index(request):
    category_list = Category.get_most_viewed()
    pages_list = Page.get_most_viewed()
    context_dict = {'categories': category_list, 'pages': pages_list}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context=context_dict)
    return response


def about(request):
    context_dict = {'boldmessage': 'about'}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    category = get_object_or_404(Category, slug=category_name_slug)

    pages = Page.objects.filter(category=category)

    context_dict['pages'] = pages
    context_dict['category'] = category
    return render(request, 'rango/category.html', context=context_dict)


@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', context={'form': form})


@login_required
def add_page(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    form = PageForm(initial={'category': category.id})

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save()
            print(page, page.url)
            return HttpResponseRedirect(reverse('show_category', args=(category_name_slug,)))
        else:
            print(form.errors)

    return render(request, 'rango/add_page.html', context={'form': form, 'category': category})


@login_required
def show_profile(request):
    user = getattr(request, 'user', None)
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None
    context_dict = {'user_profile': user_profile}

    return render(request, 'rango/profile.html', context=context_dict)
