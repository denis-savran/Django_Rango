from django.shortcuts import render
from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page
from django.urls import reverse
from django.http import HttpResponseRedirect


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': pages_list}
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {'boldmessage': 'about'}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    return render(request, 'rango/category.html', context=context_dict)


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=True)
            print(cat, cat.slug)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', context={'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
        form = PageForm(initial={'category': category.id})
    except Category.DoesNotExist:
        category = None
        form = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=True)
            print(page, page.url)
            return HttpResponseRedirect(reverse('show_category', args=(category_name_slug,)))
        else:
            print(form.errors)

    return render(request, 'rango/add_page.html',
                  context={'form': form, 'category': category})
