from django.utils.translation import gettext_lazy as _
from dynamic_preferences.types import BooleanPreference
from dynamic_preferences.preferences import Section

features = Section('features', _('Features'))


class EnableUserPreferences(BooleanPreference):
    section = features
    name = 'enable_user_preferences'
    verbose_name = _('Enable user preferences')
    default = True


class EnableSitesManger(BooleanPreference):
    section = features
    name = 'enable_sites_manager'
    verbose_name = _('Enable sites manager')
    default = True
