from __future__ import unicode_literals, absolute_import
from django.apps import AppConfig
from django.core import checks
from django.db.models.signals import post_migrate
from django.utils.module_loading import autodiscover_modules
from .sites import site
from .checks import check_cbvadmin_app


class CBVAdminConfig(AppConfig):
    name = 'cbvadmin'

    def ready(self):
        super(CBVAdminConfig, self).ready()
        # Add checks
        checks.register(check_cbvadmin_app, 'cbvadmin')
        # Autodiscover cbvadmin modules
        autodiscover_modules('cbvadmin', register_to=site)
