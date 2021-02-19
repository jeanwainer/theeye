import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theeye.settings')

app = Celery('theeye')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
