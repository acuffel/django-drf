"""
Logging settings.
"""

from logging.config import dictConfig

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # Gunicorn manages its own logs
    "formatters": {
        "console": {
            "format": "%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s",
        },
        "rich_console": {
            "format": '[%(process)d] "%(name)s"\n%(message)s',
        },
        "rich_console_django_request": {
            "format": '[%(process)d] "%(name)s" [%(status_code)d]\n%(request)s\n%(message)s',  # noqa E501
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "rich_console": {
            "class": "rich.logging.RichHandler",
            "formatter": "rich_console",
            "rich_tracebacks": True,
        },
        "rich_console_django_request": {
            "class": "rich.logging.RichHandler",
            "formatter": "rich_console_django_request",
            "rich_tracebacks": True,
        },
        "mail_admins": {
            # "level": "DEBUG",
            "class": "django.utils.log.AdminEmailHandler",
            "email_backend": "django.core.mail.backends.console.EmailBackend",
            "include_html": True,
            "filters": ["require_debug_false"],
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "rich_console",
        ],
    },
    "loggers": {
        # Django
        # https://docs.djangoproject.com/en/4.0/ref/logging/
        "django": {
            # The parent logger for messages in the django named logger hierarchy.
            # Django does not post messages using this name.
            # Instead, it uses one of the loggers below.
            "level": "NOTSET",
        },
        "django.db.backends": {
            # Messages relating to the interaction of code with the database.
            # For example, every application-level SQL statement executed by a request
            # is logged at the DEBUG level to this logger.
            # Messages to this logger have the following extra context:
            # - duration: The time taken to execute the SQL statement.
            # - sql: The SQL statement that was executed.
            # - params: The parameters that were used in the SQL call.
            # - alias: The alias of the database used in the SQL call.
            "handlers": ["null"],  # SILENT!
            "propagate": False,  # SILENT!
        },
        "django.db.backends.schema": {
            # Logs the SQL queries that are executed during schema changes to the
            # database by the migrations framework.
            # Messages to this logger have the following extra context:
            # - sql: The SQL statement that was executed.
            # - params: The parameters that were used in the SQL call.
            # - alias: The alias of the database used in the SQL call.
            "level": "INFO",
            "handlers": ["rich_console"],
        },
        "django.request": {
            # Log messages related to the handling of requests.
            # 5XX responses are raised as ERROR messages;
            # 4XX responses are raised as WARNING messages.
            # Messages to this logger have the following extra context:
            # - status_code: The HTTP response code associated with the request.
            # - request: The request object that generated the logging message.
            "level": "DEBUG",
            "handlers": ["rich_console_django_request"],
            "propagate": False,
        },
        "django.security": {
            # The security loggers will receive messages on any occurrence of
            # SuspiciousOperation and other security-related errors.
            "level": "DEBUG",
        },
        "django.server": {
            # Log messages related to the handling of requests received by the server
            # invoked by the runserver command.
            # HTTP 5XX responses are logged as ERROR messages,
            # 4XX responses are logged as WARNING messages,
            # and everything else is logged as INFO.
            # Messages to this logger have the following extra context:
            # - status_code: The HTTP response code associated with the request.
            # - request: The request object that generated the logging message.
            "level": "WARNING",
            "handlers": ["rich_console_django_request"],
            "propagate": False,
        },
        "django.template": {
            # Log messages related to the rendering of templates.
            # Missing context variables are logged as DEBUG messages.
            "level": "INFO",
        },
        "django.utils.autoreload": {
            "level": "INFO",
        },
        # Celery
        # Application 'celeryd'
        "celery": {"level": "INFO"},
        "celery.bootsteps": {
            "level": "INFO",
        },
        # Application 'celerybeat'
        "celery.beat": {
            "level": "DEBUG",
        },
        # Application 'celeryd'
        "celeryev.ev": {
            "level": "INFO",
        },
        # Celery third-party libraries
        "amqp": {
            "level": "INFO",
        },
        "kombu": {
            "level": "INFO",
        },
        "py.warnings": {
            "level": "WARNING",
        },
        # Gunicorn manages its own logs:
        # "gunicorn.access": {},
        # "gunicorn.error": {},
    },
}

# Disables Django’s logging configuration and then manually configures logging:
LOGGING_CONFIG = None


dictConfig(LOGGING)
