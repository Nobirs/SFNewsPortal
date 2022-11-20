import os

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings

from .models import PostCategory, Category, Post
from django.core.mail import EmailMultiAlternatives


@receiver(m2m_changed, sender=PostCategory)
def send_email_to_subscribers(sender, instance, **kwargs):
    print(instance.post_category.all())
    if kwargs['action'] == 'post_add':
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