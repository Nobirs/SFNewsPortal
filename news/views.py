from datetime import datetime, timedelta

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.conf import settings

from .models import Post, Author, Category
from django.urls import reverse_lazy
from .filters import PostFilter
from .forms import PostForm

import os
import logging

logger = logging.getLogger(__name__)


def user_is_author(request):
    """Return False if user is registered(but not as author).
       Return True if user is not registered or registered as Author"""
    if not request.user.is_authenticated:
        return True
    else:
        user_id = request.user.id
        try:
            author = Author.objects.get(pk=user_id)
            return True
        except ObjectDoesNotExist:
            return False


def add_new_author(request):
    new_author = Author(author_user=request.user)
    authors_group = Group.objects.get(name='authors')
    authors_group.user_set.add(request.user)
    new_author.save()
    return redirect('home')


class NewsList(ListView):
    model = Post
    ordering = '-rating'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = user_is_author(self.request)
        return context


class CategoryPostsList(ListView):
    model=Post
    ordering = '-creation_datetime'
    template_name = 'category_posts.html'
    context_object_name = 'news'
    paginate_by = 4

    def get_queryset(self):
        if not hasattr(self, 'category'):
            self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = self.category.post_set.all().order_by('-creation_datetime')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(id=self.kwargs['pk'])
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['is_author'] = user_is_author(self.request)
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.object.get_categories()
        context['is_author'] = user_is_author(self.request)
        return context

    def get_object(self, *args, **kwargs):
        logger.info("In method get_object.")
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if obj:
            logger.info(f'Get object from cache: {obj}')

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
            logger.warning(f"Object not in cached. Get object and cache it -> {obj}",)
        return obj


class NewsSearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['is_author'] = user_is_author(self.request)
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = user_is_author(self.request)
        context['post_creation_at_limit'] = Author.objects.get(author_user_id=self.request.user.id).post_creation_limit
        if context['post_creation_at_limit']:
            logger.warning("Current author cannot make more posts today...")
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        # Add category_type to form using url
        if 'create_news' in str(self.request.path):
            post.category_type = 'NW'
        elif 'create_article' in str(self.request.path):
            post.category_type = 'AR'

        # If POST is used - add post author
        if self.request.POST:
            post.post_author = Author.objects.get(author_user=self.request.user)
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'
    raise_exception = True

    def form_valid(self, form):
        post_form = form.save(commit=False)
        # Add post_categories from 'old post(in db)' if not selected
        form_categories = form.data.get('post_category', default=None)
        if form_categories is None:
            form.data['post_category'] = self.object.post_category.set()

        return super().form_valid(form)


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')
    raise_exception = True


@login_required
def subscribe(request, pk):
    category = Category.objects.get(id=pk)
    category.subscribers.add(request.user)
    return redirect(category)