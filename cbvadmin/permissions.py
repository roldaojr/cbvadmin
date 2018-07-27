from __future__ import unicode_literals
from django.db import DEFAULT_DB_ALIAS
from django.apps import apps as global_apps
from django.contrib.auth import get_permission_codename
from django.contrib.auth.management import create_permissions


def update_permissions(app_config, verbosity=2, interactive=True,
                       using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs):
    try:
        app_config = apps.get_app_config(app_config.label)
    except LookupError:
        return

    for klass in app_config.get_models():
        view_codename = get_permission_codename('view', klass._meta)
        perm = (
            view_codename,
            'Can view %s' % klass._meta.verbose_name_raw
        )
        if view_codename not in [p[0] for p in klass._meta.permissions]:
            klass._meta.permissions += (perm,)

    create_permissions(app_config, **kwargs)
