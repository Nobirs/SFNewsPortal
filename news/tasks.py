import os
from datetime import timedelta

from celery import shared_task

from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category


@shared_task
def send_email_to_subscribers(instance_pk, action_type):
    instance = Post.objects.get(id=instance_pk)
    print(instance.post_category.all())
    if action_type == 'post_add':
        categories = instance.post_category.all()
        for category in categories:
            subscribers = [user.email for user in category.subscribers.all() if user.email != ""]
            html_content = render_to_string('post_created.html',
                                            {'post': instance,
                                             'category': category.name,
                                             'link': f'{settings.SITE_URL}{str(instance.get_absolute_url())}', })

            msg = EmailMultiAlternatives(
                subject=f'Новая статья в твоём любимом разделе {category.name}!',
                body='',
                from_email=os.getenv('EMAIL_HOST_USER'),
                to=subscribers,
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@shared_task
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