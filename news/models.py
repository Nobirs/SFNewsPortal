from datetime import date

from django.contrib.auth.models import User
from django.core.cache import cache
from django.conf import settings
from django.db.models import Sum
from django.urls import reverse
from django.db import models


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = self.post_set.aggregate(postRating=Sum('rating'))
        author_rating = post_rating.get('postRating') * 3

        comment_rating = self.author_user.comment_set.aggregate(commentRating=Sum('rating'))
        author_rating += comment_rating.get('commentRating')

        for post in Post.objects.filter(post_author=self):
            for comment in Comment.objects.filter(comment_post=post):
                author_rating += comment.rating

        self.rating = author_rating
        self.save()

    def post_creation_limit(self):
        """ Return True if author cannot add another posts today.
            Post limit checked from settings POSTS_LIMIT_PER_AUTHOR."""
        today = date.today()
        todays_posts = self.post_set.filter(creation_datetime__contains=today)
        if len(todays_posts) >= settings.POSTS_LIMIT_PER_AUTHOR:
            return True
        else:
            return False

    def __str__(self):
        return self.author_user.username


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def get_absolute_url(self):
        reverse_url = reverse('category_posts', args=[str(self.id)])
        return reverse_url

    def __str__(self):
        return str(self.name)


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'News'),
        (ARTICLE, 'Article'),
    )

    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256, null=False)
    rating = models.IntegerField(default=0)
    text = models.TextField()

    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category = models.ManyToManyField(Category, through='PostCategory')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')
        print("Post was saved and deleted from cache...")

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(str(self.text)) < 125:
            return f'{self.text} ...'
        else:
            return f'{self.text[0:125]} ...'

    def get_categories(self):
        categories_names = ''
        for category in self.post_category.all():
            categories_names += category.name + ", "
        return categories_names[:-2]

    def get_categories_objects(self):
        return list(self.post_category.all())

    def get_absolute_url(self):
        reverse_url = reverse('post_detail', args=[str(self.id)])
        return reverse_url

    def get_full_url(self):
        reverse_url = self.get_absolute_url()
        return f'{settings.SITE_URL}/{reverse_url}'

    def __str__(self):
        return f'[{self.creation_datetime}] ({self.rating})  {self.title} [{self.post_author.author_user.username}]'


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    rating = models.IntegerField(default=0)
    creation_datetime = models.DateTimeField(auto_now_add=True)

    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'[{self.creation_datetime}] [{self.rating}] ({self.comment_user.username})'
