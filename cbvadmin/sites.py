from collections import defaultdict
from django.urls import include, path
from django.apps import apps
from django.views.generic import View
from menu import MenuItem


class AdminSite(object):
    namespace = 'cbvadmin'

    def __init__(self):
        self._registry = defaultdict(dict)

    def register(self, name=None, obj=None, obj_type=None):
        from .options import BaseAdmin
        if issubclass(obj, BaseAdmin):
            obj_type = 'admin'
            obj = obj(name, site=self)
        elif issubclass(obj, MenuItem):
            obj_type = 'menu'
        elif issubclass(obj, View):
            obj_type = 'view'
        if obj_type is None:
            raise TypeError('Unsupperted object type %s' % obj)
        self._registry[obj_type][name] = obj

    def register_menu(self, name, menuitem):
        self.register(name, menuitem, 'menu')

    def get_urls(self):
        urls = []
        for admin in self._registry['admin'].values():
            path_prefix = admin.get_path_prefix()
            urls.append(path(path_prefix, include(
                admin.get_urls())))
        return urls

    def get_parent_menu(self, menu_name):
        menu = self._registry['menu'].get(menu_name, None)
        if menu is not None:
            return menu
        try:
            app_config = apps.get_app_config(menu_name)
        except LookupError:
            return None
        return MenuItem(
            app_config.verbose_name, '',
            weight=getattr(app_config, 'menu_weight', 100),
            icon=getattr(app_config, 'menu_icon', None))

    def get_menu(self):
        admin_submenus = defaultdict(list)
        for _, admin in self._registry['admin'].items():
            menu_items = admin.get_menu()
            if menu_items is not None:
                for menu_item in menu_items:
                    admin_submenus[menu_item.parent].append(menu_item)

        admin_menu = []
        for menu_name, children in admin_submenus.items():
            menu = self.get_parent_menu(menu_name)
            if menu is not None:
                menu.children = children
                admin_menu.append(menu)
            else:
                admin_menu += children
        return admin_menu

    @property
    def urls(self):
        return self.get_urls(), 'cbvadmin', self.namespace


site = AdminSite()
