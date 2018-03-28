from __future__ import unicode_literals, absolute_import
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .permissions import update_permissions


class CBVAdminConfig(AppConfig):
    name = 'cbvadmin'

    def ready(self):
        super(CBVAdminConfig, self).ready()
        self.module.autodiscover()


post_migrate.connect(
    update_permissions,
    dispatch_uid='cbvadmin.permissions.update_permissions'
)
