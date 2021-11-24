# pylint: disable=protected-access
from django.apps import apps
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from menu import MenuItem
from .actions import Action
from .sites import site
from .options import SimpleAdmin, ModelAdmin
from .views.dashboard import DashboardView
from .views.user import PasswordChange
from .views.auth import (AdminLoginView, AdminLogoutView,
                         AdminPasswordResetView,
                         AdminPasswordResetDoneView,
                         AdminPasswordResetConfirmView,
                         AdminPasswordResetCompleteView)
from .utils import get_setting


class Userdmin(ModelAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email', 'is_staff',
        'is_superuser', 'last_login'
    )
    filter_fields = ('is_staff', 'is_superuser')
    menu_icon = 'fas fa-user'


class GroupAdmin(ModelAdmin):
    list_display = ('name',)
    menu_icon = 'fas fa-users'


class SiteAdmin(ModelAdmin):
    list_display = ('name', 'domain')
    menu_icon = 'fas fa-globe'
    parent_menu = None


class DashboardAdmin(SimpleAdmin):
    actions = {'dashboard': Action(DashboardView, default=True)}
    menu_icon = 'fas fa-tachometer-alt'

    def get_menu(self):
        return [
            MenuItem(
                _('Dashboard'),
                reverse(self.urls['dashboard']),
                icon=self.menu_icon
            )
        ]


class AccountsAdmin(SimpleAdmin):
    actions = {
        'login': Action(AdminLoginView),
        'logout': Action(AdminLogoutView),
        'password_change': Action(PasswordChange),
        'password_reset': Action(
            AdminPasswordResetView, path='password_reset/'),
        'password_reset_done': Action(
            AdminPasswordResetDoneView, path='password_reset/done/'),
        'password_reset_confirm': Action(
            AdminPasswordResetConfirmView, path='reset/<uidb64>/<token>'),
        'password_reset_complete': Action(
            AdminPasswordResetCompleteView, path='reset/done/')
    }

    def get_menu(self):
        return None


if '' not in site._registry['admin']:
    site.register('', DashboardAdmin)
if 'accounts' not in site._registry['admin']:
    site.register('accounts', AccountsAdmin)

if get_setting('user_admin', True):
    site.register(User, Userdmin)
if get_setting('group_admin', True):
    site.register(Group, GroupAdmin)
if get_setting('site_admin', True) and apps.is_installed('django.contrib.sites'):
    from django.contrib.sites.models import Site # NOQA
    site.register(Site, SiteAdmin)
