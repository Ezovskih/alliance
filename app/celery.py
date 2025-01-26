import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = Celery('app')

application.conf.broker_connection_retry_on_startup = True
application.config_from_object('django.conf:settings', namespace='CELERY')
application.autodiscover_tasks()
