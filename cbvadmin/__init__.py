from django.utils.module_loading import autodiscover_modules
from .sites import site
from .options import ModelAdmin
from .decorators import register

__all__ = ['site', 'ModelAdmin', 'urls', 'register']


def autodiscover():
    autodiscover_modules('cbvadmin', register_to=site)


default_app_config = 'cbvadmin.apps.CBVAdminConfig'
