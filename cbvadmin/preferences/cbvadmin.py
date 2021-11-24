from django.urls import path
from .views import PreferenceView, UserPreferenceView, SitePreferenceView
from ..options import SimpleAdmin, Action
from ..sites import site


class PreferencesAdmin(SimpleAdmin):
    actions = {
        'global': Action(PreferenceView),
        'user': Action(UserPreferenceView),
        'site': Action(SitePreferenceView),
    }

    def get_urls(self):
        urls = []
        for name, action in self.actions.items():
            urls += [
                path(
                    f'{name}/', name=name,
                    view=action.view_class.as_view(admin=self, action=name)
                ),
                path(
                    f'{name}/<section>', name=f'{name}.section',
                    view=action.view_class.as_view(admin=self, action=name)
                )
            ]
        return urls, self.namespace


site.register('preferences', PreferencesAdmin)
