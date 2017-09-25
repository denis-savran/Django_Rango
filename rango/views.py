from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.views import PasswordChangeView

from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page, UserProfile


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        # return reverse('admin')
        return reverse('show_category', args=('python',))


class MyPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        # return reverse('show_profile', urlconf='rango.urls')
        return reverse('show_profile')
        # return '/rango/profile/'
    # success_url = '/rango/profile/'


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
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
    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    return render(request, 'rango/category.html', context=context_dict)


@login_required
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


@login_required
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


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', 1))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_datetime = datetime.strptime(last_visit_cookie, '%Y-%m-%d %H:%M:%S.%f')

    if (datetime.now() - last_visit_datetime).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


@login_required
def show_profile(request):
    user = getattr(request, 'user', None)
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None
    context_dict = {'user_profile': user_profile}

    return render(request, 'rango/profile.html', context=context_dict)
