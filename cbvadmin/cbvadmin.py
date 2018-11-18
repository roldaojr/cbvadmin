from django.conf import settings
from django.urls import reverse
from menu import MenuItem
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
    dashboard_view_class = Dashboard
    default_action = 'dashboard'

    def get_actions(self):
        return {'dashboard': 'collection'}

    def get_menu(self):
        return [MenuItem('Dashboard', reverse('cbvadmin:dashboard'))]


class AccountsAdmin(SimpleAdmin):
    login_view_class = AdminLoginView
    logout_view_class = AdminLogoutView
    password_change_view_class = PasswordChange
    password_reset_view_class = AdminPasswordResetView
    password_reset_done_view_class = AdminPasswordResetDoneView
    password_reset_confirm_view_class = AdminPasswordResetConfirmView
    password_reset_complete_view_class = AdminPasswordResetCompleteView

    def get_actions(self):
        return {
            'login': 'collection',
            'logout': 'collection',
            'password_change': 'collection',
            'password_reset': 'collection',
            'password_reset_done': 'collection',
            'password_reset_confirm': 'collection',
            'password_reset_complete': 'collection'
        }

    def get_menu(self):
        return None


site.register('default', DefaultAdmin)
site.register('accounts', AccountsAdmin)


#if settings.AUTH_USER_MODEL == 'auth.User' and \
#   getattr(settings, 'CBVADMIN_REGISTER_USER', True):
#    from django.contrib.auth.models import User, Group
#    site.register(User, UserAdmin)
#    site.register(Group, GroupAdmin)
