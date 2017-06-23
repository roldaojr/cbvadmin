from django.utils.module_loading import autodiscover_modules
from .sites import site
from .options import ModelAdmin
from .decorators import register

__version__ = '0.2.0'

__all__ = ['site', 'ModelAdmin', 'urls', 'register', '__version__']

default_app_config = 'cbvadmin.apps.CBVAdminConfig'


def autodiscover():
    autodiscover_modules('cbvadmin', register_to=site)
