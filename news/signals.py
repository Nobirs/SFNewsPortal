from django.db.models.signals import m2m_changed
from django.dispatch import receiver


from .models import PostCategory, Category, Post
from .tasks import send_email_to_subscribers


@receiver(m2m_changed, sender=PostCategory)
def new_post_added(sender, instance, **kwargs):
    print("New post was added... Trying to send mails...")
    send_email_to_subscribers.delay(instance.pk, kwargs['action'])