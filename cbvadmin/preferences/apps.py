from django.apps import AppConfig
from dynamic_preferences.registries import preference_models
from .registries import site_preferences_registry


class SitePreferencesConfig(AppConfig):
    name = 'cbvadmin.preferences'

    def ready(self):
        SitePreference = self.get_model('SitePreference')
        preference_models.register(SitePreference, site_preferences_registry)
