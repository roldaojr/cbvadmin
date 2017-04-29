from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .options import ModelAdmin
from .decorators import register


@register(User)
class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'active')

    def get_form_class(self, request, obj=None, **kwargs):
        if obj:
            return UserChangeForm
        else:
            return UserCreationForm


@register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ('name',)
