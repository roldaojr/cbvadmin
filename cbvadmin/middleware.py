from django.apps import apps
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sites.requests import RequestSite


class CurrentSiteMiddleware(MiddlewareMixin):
    """
    Middleware that sets `site` attribute to request object.
    """

    def _get_current_site(self, request):
        if apps.is_installed('django.contrib.sites'):
            from django.contrib.sites.models import Site # NOQA
            try:
                return Site.objects.get_current(request)
            except Site.DoesNotExist:
                pass

        return RequestSite(request)

    def process_request(self, request):
        request.site = self._get_current_site(request)
