from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title',
                  'text',
                  'rating',
                  'post_category',
                  ]

    def is_valid(self):
        return super().is_valid()