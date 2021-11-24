from django.apps import AppConfig, apps
from django.utils.module_loading import autodiscover_modules
from .dashboard import wdigets_registry
from .sites import site as admin_site
from .utils import get_setting


class CBVAdminConfig(AppConfig):
    name = 'cbvadmin'

    def ready(self):
        super().ready()
        # Autodiscover cbvadmin modules
        if get_setting('LOAD_ADMIN_MODULE', True):
            autodiscover_modules('admin', register_to=admin_site)
        autodiscover_modules('cbvadmin', register_to=admin_site)
        # discover dashboard widgets
        app_names = [app.name for app in apps.app_configs.values()]
        wdigets_registry.autodiscover(app_names)
