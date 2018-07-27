from django.core import checks
from django.conf import settings

E001 = checks.Error(
    "Missing 'CBVADMIN_TEMPLATE_PACK' setting", obj='cbvadmin')


def check_cbvadmin_app(**kwargs):
    errors = []
    if not hasattr(settings, 'CBVADMIN_TEMPLATE_PACK'):
        errors.append(E001)
    return errors
