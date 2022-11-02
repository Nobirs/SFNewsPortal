from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import classonlymethod
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    ordering = '-rating'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.object.get_categories()
        return context


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
        return context


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        # Add category_type to form using url
        if 'news' in str(self.request.path):
            post.category_type = 'NW'
        elif 'articles' in str(self.request.path):
            post.category_type = 'AR'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'

    def form_valid(self, form):
        post_form = form.save(commit=False)
        # Add post_categories from 'old post(in db)' if not selected
        form_categories = form.data.get('post_category', default=None)
        if form_categories is None:
            form.data['post_category'] = self.object.post_category.set()

        return super().form_valid(form)


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')


def update_redirect_nw_ar_if_needed(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.category_type == 'NW' and 'news' not in request.path:
        return HttpResponseRedirect(f'/news/{pk}/update/')
    elif post.category_type == 'AR' and 'articles' not in request.path:
        return HttpResponseRedirect(f'/articles/{pk}/update/')
    else:
        view = PostUpdate.as_view()
        return view(request, pk=pk)


def delete_redirect_nw_ar_if_needed(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.category_type == 'NW' and 'news' not in request.path:
        return HttpResponseRedirect(f'/news/{pk}/delete/')
    elif post.category_type == 'AR' and 'articles' not in request.path:
        return HttpResponseRedirect(f'/articles/{pk}/delete/')
    else:
        view = PostDelete.as_view()
        return view(request, pk=pk)