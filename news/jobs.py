import os
from datetime import date, timedelta

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings

from .models import Category, Post


def send_week_post_updates():
    for category in Category.objects.all():
        # get list of email address of all subscribers in category
        subscribers = [user.email for user in category.subscribers.all() if user.email != ""]
        day_week_ago = timezone.now() - timedelta(weeks=1)
        week_posts = category.post_set.filter(creation_datetime__gte=day_week_ago)

        html_content = render_to_string('week_posts.html',
                                        {'posts': week_posts,
                                         'category': category.name,
                                         })
        msg = EmailMultiAlternatives(
            subject = f'Список новостей за последнюю неделю в разделе {category.name}',
            body='',
            from_email=settings.EMAIL_HOST_USER,
            to=subscribers,
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
