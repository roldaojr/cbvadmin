from .sites import site
from .options import ModelAdmin
from .decorators import register

__version__ = '0.4.0a1'

__all__ = ['site', 'ModelAdmin', 'urls', 'register', '__version__']

default_app_config = 'cbvadmin.apps.CBVAdminConfig'
