from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.http import require_GET, require_safe
from elasticsearch_dsl.query import Q
from registration.backends.simple.views import RegistrationView

from rango.documents import (CategoryDocument, PageDocument,
                             search_all_doc_types)
from rango.forms import CategoryForm, PageForm, UserProfileForm
from rango.models import Category, Page, UserProfile
from rango.utils import resize_image, visitor_cookie_handler


@require_safe
def index(request):
    category_list = Category.get_most_viewed()
    pages_list = Page.get_most_viewed()
    context_dict = {'categories': category_list, 'pages': pages_list}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context=context_dict)
    return response


@require_safe
def about(request):
    context_dict = {'boldmessage': 'about'}
    return render(request, 'rango/about.html', context=context_dict)


@require_safe
def show_category(request, category_name_slug):
    context_dict = {}
    category = get_object_or_404(Category, slug=category_name_slug)

    pages = Page.objects.filter(category=category)

    context_dict['pages'] = pages
    context_dict['category'] = category
    return render(request, 'rango/category.html', context=context_dict)


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return index(request)
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', context={'form': form})


@login_required
def add_page(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save()
            return redirect('show_category', category_name_slug)
        else:
            print(form.errors)
    else:
        form = PageForm(initial={'category': category.id})

    return render(request, 'rango/add_page.html', context={'form': form, 'category': category})


@login_required
@require_GET
def show_profile(request):
    try:
        # user_profile = get_object_or_404(UserProfile, user=request.user)
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    context_dict = {'user_profile': user_profile}

    return render(request, 'rango/profile.html', context=context_dict)


@require_GET
def search(request):
    context_dict = {}
    category_list = Category.objects.values_list('name', flat=True)
    context_dict['category_list'] = category_list

    q = request.GET.get('q')
    if q:
        if len(request.GET) == 1:
            search_result = search_all_doc_types(q)
            context_dict.update(search_result)
        else:
            category = request.GET.get('category')
            if category:
                complex_query = Q('bool', must=[Q('match', category__name=category), Q('match', title=q)])
                search_result = PageDocument.search().filter(complex_query).to_queryset()
                context_dict['pages'] = search_result
            else:
                if request.GET.get('categories'):
                    search_result = CategoryDocument.search().filter('match', name=q).to_queryset()
                    context_dict['categories'] = search_result
                if request.GET.get('pages'):
                    search_result = PageDocument.search().filter('match', title=q).to_queryset()
                    context_dict['pages'] = search_result
    return render(request, 'rango/search.html', context=context_dict)


@require_GET
def track_url(request):
    page_id = request.GET.get('page_id')

    if page_id:
        page = get_object_or_404(Page, id=page_id)
        page.views += 1
        page.save()
        redirect_url = page.get_url()
    else:
        redirect_url = reverse('index')

    return redirect(redirect_url)


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user=None):
        redirect_link = reverse('edit_profile')
        # Add GET parameter to get customized edit_profile
        redirect_link = redirect_link + '?new_user=1'
        return redirect_link


@login_required
def edit_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            update_fields = []
            website = request.POST.get('website')
            picture = request.FILES.get('picture')
            if website:
                user_profile.website = website
                update_fields.append('website')
            if picture:
                # Delete old profile picture if it exists
                if user_profile.picture:
                    user_profile.picture.delete()

                picture = resize_image(picture)

                user_profile.picture = picture
                update_fields.append('picture')
            if update_fields:
                user_profile.save(update_fields=update_fields)
            return redirect('show_profile')
    else:
        form = UserProfileForm()
    return render(request, 'rango/edit_profile.html', context={'form': form,
                                                               'user_profile': user_profile,
                                                               'new_user': request.GET.get('new_user')})
