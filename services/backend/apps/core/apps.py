from django.apps import AppConfig
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = "core"
    verbose_name = _("Core app")
    main_menu_items = [
        {
            "priority": 0,
            "title": _("Home"),
            "url": reverse_lazy("core:home"),
            "icon": "fa-solid fa-home",
        },
    ]

    def ready(self):
        import core.signals.handlers  # noqa: F401
