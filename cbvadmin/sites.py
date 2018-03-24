from __future__ import unicode_literals
import six
from collections import defaultdict
from django.conf.urls import url, include
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import reverse
from menu import MenuItem
from .options import BaseAdmin
from .views.dashboard import Dashboard
from .views.user import PasswordChange
from .utils import get_setting, menu_generator


class AdminSite(object):
    _registry = {}
    name = 'cbvadmin'
    title = 'CBVAdmin'
    login_form = None
    _menu_registry = defaultdict(lambda: menu_generator)
    dashboard_view_class = Dashboard
    passwordchange_view_class = PasswordChange

    def register(self, model_class, admin_class):
        admin = admin_class(model_class)
        admin.site = self
        self._registry[model_class] = admin

    def register_menu(self, app_label, menu_func):
        self._menu_registry[app_label] = menu_func

    def get_urls(self):
        this_admin = BaseAdmin(site=self)
        kwargs = {'admin': this_admin}
        dashboard_view = self.dashboard_view_class.as_view(**kwargs)
        password_change_view = self.passwordchange_view_class.as_view(**kwargs)
        urls = [
            url(r'^$', dashboard_view, name='dashboard'),
            url(r'^login$', self.login, name='login'),
            url(r'^logout$', self.logout, name='logout'),
            url(r'^password$', password_change_view, name='password_change')
        ]
        for model, admin in six.iteritems(self._registry):
            model_name = (model._meta.app_label,
                          model._meta.model_name)
            urls.append(url('%s/%s/' % model_name, include(admin.get_urls())))
        return urls

    def get_menu(self):
        admin_menu = [MenuItem('Dashboard', reverse('cbvadmin:dashboard'))]
        admin_sub_menus = defaultdict(lambda: [])
        for model, admin in six.iteritems(self._registry):
            app_label = model._meta.app_label
            sub_menu = admin.get_menu()
            if sub_menu:
                admin_sub_menus[app_label] += tuple(sub_menu)
        for label, items in sorted(six.iteritems(admin_sub_menus)):
            admin_menu += self._menu_registry[label](label, items)
        return admin_menu

    @property
    def urls(self):
        return self.get_urls(), 'cbvadmin', self.name

    def login(self, request):
        THEME = get_setting('theme', 'semantic-ui')
        from django.contrib.auth.views import login
        context = {}
        if (REDIRECT_FIELD_NAME not in request.GET and
                REDIRECT_FIELD_NAME not in request.POST):
            context[REDIRECT_FIELD_NAME] = reverse('cbvadmin:dashboard')
        kwargs = {
            'extra_context': context,
            'template_name': 'cbvadmin/%s/login.html' % THEME
        }
        request.current_app = self.name
        return login(request, **kwargs)

    def logout(self, request):
        from django.contrib.auth.views import logout_then_login
        return logout_then_login(request, login_url=reverse('cbvadmin:login'))


site = AdminSite()
