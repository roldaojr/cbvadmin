from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from dynamic_preferences.models import PerInstancePreferenceModel


class SitePreference(PerInstancePreferenceModel):
    instance = models.ForeignKey(Site, on_delete=models.CASCADE)

    class Meta(PerInstancePreferenceModel.Meta):
        app_label = 'preferences'
        verbose_name = _("site preference")
        verbose_name_plural = _("site preferences")
