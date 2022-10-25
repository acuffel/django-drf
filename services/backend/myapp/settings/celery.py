"""
Celery settings.
"""

import os

# RabbitMQ
RABBITMQ_HOST = str(os.environ.get("RABBITMQ_HOST", "brocker"))
RABBITMQ_PORT = int(os.environ.get("RABBITMQ_PORT", "5672"))
RABBITMQ_DEFAULT_VHOST = str(os.environ.get("RABBITMQ_DEFAULT_VHOST", "my_vhost"))
RABBITMQ_DEFAULT_USER = str(os.environ.get("RABBITMQ_DEFAULT_USER", "guest"))
RABBITMQ_DEFAULT_PASS = str(os.environ.get("RABBITMQ_DEFAULT_PASS", "guest"))

# Celery
CELERY_BROKER_URL = "amqp://{user}:{password}@{host}:{port}/{vhost}".format(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    vhost=RABBITMQ_DEFAULT_VHOST,
    user=RABBITMQ_DEFAULT_USER,
    password=RABBITMQ_DEFAULT_PASS,
)
CELERY_TASK_DEFAULT_QUEUE = "gateway"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 24 * 60 * 60  # one day

# Configure Celery to use the django-celery-results backend:
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXPIRES = 24 * 60 * 60  # one day
CELERY_RESULT_PERSISTENT = True
CELERY_CACHE_BACKEND = "django-cache"
