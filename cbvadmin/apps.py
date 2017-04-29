from __future__ import unicode_literals, absolute_import
from django.apps import AppConfig


class CBVAdminConfig(AppConfig):
    name = 'cbvadmin'

    def ready(self):
        super(CBVAdminConfig, self).ready()
        self.module.autodiscover()
