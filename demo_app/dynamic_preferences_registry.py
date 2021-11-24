from django.conf.global_settings import LANGUAGES
from django.utils.translation import gettext_lazy as _
from dynamic_preferences.types import (
    BooleanPreference, ChoicePreference, FilePreference, Section
)
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.users.registries import user_preferences_registry
from cbvadmin.preferences.registries import site_preferences_registry
from cbvadmin.dynamic_preferences_registry import features

branding = Section('branding', 'Branding')


@global_preferences_registry.register
class EnableUserRegistration(BooleanPreference):
    section = features
    name = 'enable_registration'
    verbose_name = _('Enable user registration')
    default = True


@user_preferences_registry.register
class Language(ChoicePreference):
    name = 'language'
    choices = LANGUAGES
    default = 'en'


@site_preferences_registry.register
class SiteLogo(FilePreference):
    section = branding
    name = 'logo'
    default = None
