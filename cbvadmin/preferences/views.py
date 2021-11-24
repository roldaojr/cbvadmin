from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
from django.contrib import messages
from dynamic_preferences.views import PreferenceFormView
from dynamic_preferences.forms import (
    GlobalPreferenceForm, preference_form_builder
)
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.users.views import UserPreferenceFormView
from dynamic_preferences.users.forms import UserPreferenceForm
from dynamic_preferences.users.registries import user_preferences_registry
from cbvadmin.views.mixins import AdminMixin, PermissionRequiredMixin
from .forms import SitePreferenceForm
from .registries import site_preferences_registry


class PreferenceFormMixin:
    def dispatch(self, request, *args, **kwargs):
        section = self.kwargs.get('section', None)
        if not section:
            if len(self.registry.section_objects) > 0:
                section = next(iter(self.registry.section_objects.keys()))
        kwargs['section'] = section
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Preferences saved')
        return super().form_valid(form)


class PreferenceView(PermissionRequiredMixin, PreferenceFormMixin, AdminMixin, PreferenceFormView):
    form_class = GlobalPreferenceForm
    registry = global_preferences_registry
    title = 'Global Preferences'

    def has_permission(self):
        return self.request.user.is_superuser


class UserPreferenceView(PreferenceFormMixin, AdminMixin, UserPreferenceFormView):
    form_class = UserPreferenceForm
    registry = user_preferences_registry
    title = 'User Preferences'

    def get_form_class(self, *args, **kwargs):
        form_class = preference_form_builder(
            UserPreferenceForm,
            instance=self.request.user,
            section=self.kwargs.get('section', None)
        )
        return form_class


class SitePreferenceView(PermissionRequiredMixin, PreferenceFormMixin, AdminMixin, PreferenceFormView):
    registry = site_preferences_registry
    title = 'Site Preferences'

    def has_permission(self):
        return self.request.user.is_superuser

    def get_form_class(self, *args, **kwargs):
        print('section', self.section)
        if 'site' in self.kwargs:
            self.site = get_object_or_404(Site, pk=self.kwargs['site'])
        else:
            self.site = self.request.site
        if hasattr(self.site, 'pk'):
            return preference_form_builder(
                SitePreferenceForm,
                instance=self.site,
                section=self.section.name
            )
        return SitePreferenceForm
