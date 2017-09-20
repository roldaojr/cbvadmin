from django.conf import settings
from .sites import site
from .options import UserAdmin, GroupAdmin


if settings.AUTH_USER_MODEL == 'auth.User' and \
   getattr(settings, 'CBVADMIN_REGISTER_USER', True):
    from django.contrib.auth.models import User, Group
    site.register(User, UserAdmin)
    site.register(Group, GroupAdmin)
