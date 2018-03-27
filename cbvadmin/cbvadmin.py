from django.conf import settings
from django.urls import reverse
from menu import MenuItem
from .sites import site
from .options import SimpleAdmin, UserAdmin, GroupAdmin
from .views.dashboard import Dashboard
from .views.user import PasswordChange


class DefaultAdmin(SimpleAdmin):
    dashboard_view_class = Dashboard
    password_change_view_class = PasswordChange

    default_action = 'dashboard'

    def get_actions(self):
        return {
            'dashboard': 'collection',
            'password_change': 'collection'
        }

    def get_menu(self):
        return [MenuItem('Dashboard', reverse('cbvadmin:dashboard'))]


site.register('default', DefaultAdmin)


if settings.AUTH_USER_MODEL == 'auth.User' and \
   getattr(settings, 'CBVADMIN_REGISTER_USER', True):
    from django.contrib.auth.models import User, Group
    site.register(User, UserAdmin)
    site.register(Group, GroupAdmin)
