from django.apps import apps


def get_main_menu_items():
    main_menu_items = []
    for app_configs in apps.get_app_configs():
        if hasattr(app_configs, "main_menu_items"):
            main_menu_items.extend(app_configs.main_menu_items)
    return sorted(main_menu_items, key=lambda d: d["priority"])


def menu(request):
    return {
        "main_menu_items": get_main_menu_items(),
    }
