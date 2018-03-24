from __future__ import unicode_literals
from django.contrib.auth.management import create_permissions


def update_permissions(app_config, **kwargs):
    for model in app_config.get_models():
        view_permission = 'view_%s' % model._meta.model_name
        if view_permission not in [p[0] for p in model._meta.permissions]:
            model._meta.permissions += [
                (view_permission, 'Can view %s' % model._meta.verbose_name)
            ]

    create_permissions(app_config, **kwargs)
