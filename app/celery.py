import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = Celery('app')  # broker_url='redis://127.0.0.1:6379/0'

application.conf.broker_connection_retry_on_startup = True
application.config_from_object("django.conf:settings", namespace='CELERY')
application.autodiscover_tasks()
