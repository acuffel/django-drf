import os
import time

from celery import Celery
from celery.signals import setup_logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")

app = Celery("myapp")
app.config_from_object("django.conf:settings", namespace="CELERY")


# Completely disables Celery logging configuration:
# https://docs.celeryq.dev/en/stable/userguide/tasks.html#logging
@setup_logging.connect
def on_setup_logging(**kwargs):
    pass


app.autodiscover_tasks()


@app.task(bind=True, queue="gateway")
def debug_task(self):
    time.sleep(1)
    return vars(self.request)


@app.task(bind=True, queue="computation")
def debug_long_task(self):
    time.sleep(5)
    return vars(self.request)
