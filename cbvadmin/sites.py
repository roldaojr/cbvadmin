from __future__ import unicode_literals
import six
from django.apps import apps
from django.core.urlresolvers import reverse
from django.conf.urls import url, include
from menu import MenuItem
from .options import BaseAdmin
from .views.dashboard import Dashboard


class AdminSite(object):
    _registry = {}
    name = 'cbvadmin'
    title = 'CBVAdmin'

    def register(self, model_class, admin_class):
        admin = admin_class(model_class)
        admin.site = self
        self._registry[model_class] = admin

    def get_urls(self):
        dashboard_view = Dashboard.as_view(admin=BaseAdmin(site=self))
        urls = [url(r'^$', dashboard_view, name='dashboard')]
        for model, admin in self._registry.iteritems():
            model_name = (model._meta.app_label,
                          model._meta.model_name)
            urls.append(url('%s/%s/' % model_name, include(admin.get_urls())))
        return urls

    def get_menu(self):
        admin_menu = [MenuItem('Dashboard', reverse('cbvadmin:dashboard'))]
        admin_sub_menus = {}
        for model, admin in self._registry.iteritems():
            app_label = model._meta.app_label
            app_title = apps.get_app_config(app_label).verbose_name
            if app_title not in admin_sub_menus:
                admin_sub_menus[app_title] = []
            admin_sub_menus[app_title] += [admin.get_menu_item()]
        for label, items in sorted(six.iteritems(admin_sub_menus)):
            admin_menu.append(MenuItem(label, '', children=items))
        return admin_menu

    @property
    def urls(self):
        return self.get_urls(), 'cbvadmin', self.name


site = AdminSite()
