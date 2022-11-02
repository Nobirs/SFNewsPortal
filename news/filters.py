from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter
from django.forms import DateTimeInput

from .models import Post, Category


class PostFilter(FilterSet):
    posted_after = DateTimeFilter(
        field_name="creation_datetime",
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%d %H-%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    post_category = ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'post_category': ['exact'],
        }