from django.conf import settings


def get_setting(key, default=None):
    return getattr(settings, 'CBVADMIN_%s' % key.upper(), default)
