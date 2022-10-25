import multiprocessing


# Server Socket
# https://docs.gunicorn.org/en/stable/settings.html#server-socket

# The socket to bind.
# bind = ["127.0.0.1:8000"]  # Default
bind = ["0.0.0.0:8000"]

# The maximum number of pending connections.
backlog = 2048

# The number of worker processes for handling requests.
# A positive integer generally in the 2-4 x $(NUM_CORES) range. You’ll want to vary this
# a bit to find the best for your particular application’s work load.
# workers = 1  # Default
workers = multiprocessing.cpu_count() * 2 + 1

# The type of workers to use.
worker_class = "sync"  # Default


# Server Mechanics
# https://docs.gunicorn.org/en/stable/settings.html#server-mechanics

# Daemonize the Gunicorn process.
daemon = False  # Default


# Debugging
# https://docs.gunicorn.org/en/stable/settings.html#debugging

# Restart workers when code changes.
# reload = False  # Default
reload = True

# The implementation that should be used to power reload.
reload_engine = "auto"  # Default

# Extends reload option to also watch and reload on additional files.
reload_extra_files = []  # Default

# Install a trace function that spews every line executed by the server.
spew = False  # Default

# Logging
# https://docs.gunicorn.org/en/stable/settings.html#logging

# The Access log file to write to.
# '-' means log to stdout.
# accesslog = None  # Default
# accesslog = "-"

# Disable redirect access logs to syslog.
disable_redirect_access_to_syslog = False  # Default

# The access log format.
# access_log_format = (
#     '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'  # Default
# )
# access_log_format = (
#     '%(h)s\n%(l)s\n%(u)s\n%(t)s\n"%(r)s"\n%(s)s\n%(b)s\n"%(f)s"\n"%(a)s"'
# )

# The Error log file to write to.
# '-' means log to stderr.
errorlog = "-"  # Default

# The granularity of Error log outputs.
loglevel = "debug"  # Default

# Redirect stdout/stderr to specified file in errorlog.
capture_output = False  # Default

# The logger you want to use to log events in Gunicorn.
logger_class = "gunicorn.glogging.Logger"  # Default

# The log config dictionary to use, using the standard Python logging module’s
# dictionary configuration format. This option takes precedence over the logconfig
# option, which uses the older file configuration format.
# logconfig_dict = {}  # Default

# https://github.com/benoitc/gunicorn/blob/master/examples/logging.conf
logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "rich_console": {
            "format": '[%(process)d] "%(name)s"\n%(message)s',
        },
        "gunicorn_access_default": {
            "format": '[%(process)d] "%(name)s"\n%(message)s',
        },
    },
    "handlers": {
        "rich_console": {
            "class": "rich.logging.RichHandler",
            "formatter": "rich_console",
            "rich_tracebacks": True,
        },
        "gunicorn_access_default": {
            "class": "logging.StreamHandler",
            "formatter": "gunicorn_access_default",
        },
    },
    "root": {
        "level": "NOTSET",
    },
    "loggers": {
        "gunicorn.access": {
            "level": "NOTSET",
            "propagate": False,
            "handlers": [
                "rich_console",
                # "gunicorn_access_default",
            ],
        },
        "gunicorn.error": {
            "level": "INFO",
            "propagate": False,
            "handlers": [
                "rich_console",
            ],
        },
    },
}

# Address to send syslog messages.
syslog_addr = "udp://localhost:514"  # Default

# Send Gunicorn logs to syslog.
syslog = False  # Default

# Makes Gunicorn use the parameter as program-name in the syslog entries.
syslog_prefix = None  # Default

# Syslog facility name
syslog_facility = "user"  # Default

# Enable inheritance for stdio file descriptors in daemon mode.
enable_stdio_inheritance = False  # Default

# host:port of the statsd server to log to.
statsd_host = None  # Default

# Prefix to use when emitting statsd metrics (a trailing . is added, if not provided).
statsd_prefix = ""  # Default


# Process Naming
# https://docs.gunicorn.org/en/stable/settings.html#process-naming

# A base to use with setproctitle for process naming.
proc_name = None  # Default

# Internal setting that is adjusted for each type of application.
default_proc_name = "gunicorn"  # Default


# SSL
# https://docs.gunicorn.org/en/stable/settings.html#ssl


# Security
# https://docs.gunicorn.org/en/stable/settings.html#security

# The maximum size of HTTP request line in bytes.
limit_request_line = 4094  # Default

# Limit the number of HTTP headers fields in a request.
limit_request_fields = 100  # Default

# Limit the allowed size of an HTTP request header field.
limit_request_field_size = 8190  # Default


# Server Hooks
# https://docs.gunicorn.org/en/stable/settings.html#server-hooks

# Called just before the master process is initialized.
def on_starting(server):
    pass


# Called to recycle workers during a reload via SIGHUP.
def on_reload(server):
    pass


# Called just after the server is started.
def when_ready(server):
    pass


# Called just before a worker is forked.
def pre_fork(server, worker):
    pass


# Called just after a worker has been forked.
def post_fork(server, worker):
    pass


# Called just after a worker has initialized the application.
def post_worker_init(worker):
    pass


# Called just after a worker exited on SIGINT or SIGQUIT.
def worker_int(worker):
    pass


# Called when a worker received the SIGABRT signal.
def worker_abort(worker):
    pass


# Called just before a new master process is forked.
def pre_exec(server):
    pass


# Called just before a worker processes the request.
def pre_request(worker, req):
    worker.log.debug("%s %s" % (req.method, req.path))


# Called after a worker processes the request.
def post_request(worker, req, environ, resp):
    pass


# Called just after a worker has been exited, in the master process.
def child_exit(server, worker):
    pass


# Called just after a worker has been exited, in the worker process.
def worker_exit(server, worker):
    pass


# Called just after num_workers has been changed.
def nworkers_changed(server, new_value, old_value):
    pass


# Called just before exiting Gunicorn.
def on_exit(server):
    pass
