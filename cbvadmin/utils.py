from collections import defaultdict
from django.conf import settings
from django.apps import apps
from menu import MenuItem


def get_setting(key, default=None):
    return getattr(settings, 'CBVADMIN_%s' % key.upper(), default)


def menu_generator(app_label, items):
    app_config = apps.get_app_config(app_label)
    app_title = app_config.verbose_name
    weight = getattr(app_config, 'menu_weight', 50)
    menu_items = []
    submenu_items = defaultdict(list)
    for item in items:
        if hasattr(item, 'submenu'):
            if isinstance(item.submenu, str):
                submenu_items[item.submenu].append(item)
            elif item.submenu is False:
                menu_items.append(item)
        else:
            submenu_items[app_title].append(item)

    return menu_items + [
        MenuItem(app_title, '', children=subitems, weight=weight)
        for app_title, subitems in submenu_items.items()
    ]
