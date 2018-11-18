from .sites import site
from .decorators import register
from ._version import get_versions

__all__ = ['site', 'urls', 'register', '__version__']

__version__ = get_versions()['version']

default_app_config = 'cbvadmin.apps.CBVAdminConfig'
