from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from cbvadmin.dashboard import DashboardWidget, wdigets_registry


@wdigets_registry.register(name='users_count')
class TotalUserCount(DashboardWidget):
    template_name = 'dashboard/widget.html'
    order = 1

    def get_context_data(self, **kwargs):
        return {
            'color': 'green',
            'icon': 'fas fa-user',
            'title': _('users'),
            'value': User.objects.count()
        }


@wdigets_registry.register(name='groups_count')
class TotalGroupCount(DashboardWidget):
    template_name = 'dashboard/widget.html'
    order = 2

    def get_context_data(self, **kwargs):
        return {
            'color': 'cyan',
            'icon': 'fas fa-users',
            'title': _('groups'),
            'value': Group.objects.count()
        }


@wdigets_registry.register(name='sites_count')
class TotalSiteCount(DashboardWidget):
    template_name = 'dashboard/widget.html'
    order = 2

    def get_context_data(self, **kwargs):
        return {
            'color': 'blue',
            'icon': 'fas fa-globe',
            'title': _('sites'),
            'value': Site.objects.count()
        }
