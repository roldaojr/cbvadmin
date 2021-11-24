from dynamic_preferences.forms import (
    GlobalPreferenceForm as BaseGlobalPreferenceForm,
    PreferenceForm
)
from dynamic_preferences.users.forms import (
    UserPreferenceForm as BaseUserPreferenceForm
)
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.users.registries import user_preferences_registry
from .registries import site_preferences_registry


class GlobalPreferenceForm(BaseGlobalPreferenceForm):
    registry = global_preferences_registry


class UserPreferenceForm(BaseUserPreferenceForm):
    registry = user_preferences_registry


class SitePreferenceForm(PreferenceForm):
    registry = site_preferences_registry
