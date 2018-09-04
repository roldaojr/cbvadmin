from collections import defaultdict
from django.conf.urls import url, include
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import reverse
from .utils import get_setting, menu_generator


class AdminSite(object):
    _registry = {}
    _simple_registry = {}
    _menu_registry = defaultdict(lambda: menu_generator)

    def __init__(self):
        self.name = get_setting('SITE_NAME', 'cbvadmin')
        self.title = get_setting('SITE_TITLE', 'CBVAdmin')

    def register(self, model_class=None, admin_class=None):
        admin = admin_class(model_class)
        admin.site = self
        if isinstance(model_class, str) or model_class is None:
            self._simple_registry[model_class] = admin
        else:
            self._registry[model_class] = admin

    def register_menu(self, app_label, menu_func):
        self._menu_registry[app_label] = menu_func

    def get_urls(self):
        urls = []
        for name, admin in self._simple_registry.items():
            if name == 'default':
                urls.append(url('', include(admin.get_urls())))
            else:
                urls.append(url('%s/' % name, include(admin.get_urls())))
        for model, admin in self._registry.items():
            model_name = (model._meta.app_label,
                          model._meta.model_name)
            urls.append(url('%s/%s/' % model_name, include(admin.get_urls())))
        return urls

    def get_menu(self):
        admin_menu = []
        admin_sub_menus = defaultdict(lambda: [])
        for name, admin in self._simple_registry.items():
            items = admin.get_menu()
            if items:
                admin_menu += items

        for model, admin in self._registry.items():
            app_label = model._meta.app_label
            sub_menu = admin.get_menu()
            if sub_menu:
                admin_sub_menus[app_label] += tuple(sub_menu)

        for label, items in sorted(admin_sub_menus.items()):
            admin_menu += self._menu_registry[label](label, items)
        return admin_menu

    @property
    def urls(self):
        return self.get_urls(), 'cbvadmin', self.name


site = AdminSite()
