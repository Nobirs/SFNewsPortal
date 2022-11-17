from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    ordering = '-rating'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['is_authenticated'] = self.request.user.is_authenticated
    #     return context


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


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'
    raise_exception = True

    def form_valid(self, form):
        post = form.save(commit=False)
        # Add category_type to form using url
        if 'create_news' in str(self.request.path):
            post.category_type = 'NW'
        elif 'create_article' in str(self.request.path):
            post.category_type = 'AR'

        # If POST is used - add post author
        if self.request.POST:
            print(self.request.POST)
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