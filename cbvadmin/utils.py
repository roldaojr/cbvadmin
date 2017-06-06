from django.conf import settings
from django.apps import apps
from menu import MenuItem


def get_setting(key, default=None):
    return getattr(settings, 'CBVADMIN_%s' % key.upper(), default)


def plain_menu_generator(app_label, items):
    app_config = apps.get_app_config(app_label)
    weight = getattr(app_config, 'menu_weight', 0)
    for item in items:
        item.weight += weight
    return items


def sub_menu_generator(app_label, items):
    app_config = apps.get_app_config(app_label)
    app_title = app_config.verbose_name
    weight = getattr(app_config, 'menu_weight', 50)
    return [MenuItem(app_title, '', children=items, weight=weight)]
