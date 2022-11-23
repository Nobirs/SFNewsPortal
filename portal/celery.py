import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal.settings')

app = Celery('portal')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_week_updates_to_subscribers': {
        'task': 'news.tasks.send_week_post_updates',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}
