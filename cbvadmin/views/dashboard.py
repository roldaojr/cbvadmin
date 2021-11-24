from django.views.generic import TemplateView
from cbvadmin.views.mixins import AdminMixin
from ..dashboard import wdigets_registry


class DashboardView(AdminMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registered_widgets = sorted(
            wdigets_registry.values(),
            key=lambda i: i.order
        )
        widgets = []
        for widget_class in registered_widgets:
            widgets.append(widget_class(self.request))

        return super().get_context_data(
            widgets=widgets, **context
        )
