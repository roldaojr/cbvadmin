# pylint: disable=protected-access
from django.urls import reverse
from menu import MenuItem
from .actions import Action
from .sites import site
from .options import SimpleAdmin
from .views.dashboard import Dashboard
from .views.user import PasswordChange
from .views.auth import (AdminLoginView, AdminLogoutView,
                         AdminPasswordResetView,
                         AdminPasswordResetDoneView,
                         AdminPasswordResetConfirmView,
                         AdminPasswordResetCompleteView)


class DefaultAdmin(SimpleAdmin):
    default_action = 'dashboard'
    actions = {'dashboard': Action(Dashboard, default=True)}

    def get_menu(self):
        return [MenuItem('Dashboard', reverse(self.urls['dashboard']))]


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
    site.register('', DefaultAdmin)
if 'accounts' not in site._registry['admin']:
    site.register('accounts', AccountsAdmin)
