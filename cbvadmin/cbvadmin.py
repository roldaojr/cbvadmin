from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .options import ModelAdmin
from .sites import site


class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'active')

    def get_form_class(self, request, obj=None, **kwargs):
        if obj:
            return UserChangeForm
        else:
            return UserCreationForm


class GroupAdmin(ModelAdmin):
    list_display = ('name',)


if settings.AUTH_USER_MODEL == 'auth.User' and getattr(settings, 'CBVADMIN_REGISTER_USER', True):
    from django.contrib.auth.models import User, Group
    site.register(User, UserAdmin)
    site.register(Group, GroupAdmin)
