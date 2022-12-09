from django.contrib import admin
from .models import Author, Category, Comment, PostCategory, Post


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['author_user', 'rating', 'post_creation_limit']
    search_fields = ['author_user__username']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]
    list_filter = ['rating', 'creation_datetime']
    search_fields = ['text']


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PostCategory._meta.get_fields()]
    list_filter = ['category_through__name']


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'rating', 'creation_datetime', 'category_type', 'post_author']
    list_filter = ['rating', 'creation_datetime', 'category_type']
    search_fields = ['title__icontains', 'text__icontains']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostAdmin)
