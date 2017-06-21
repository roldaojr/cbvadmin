from django.views.generic import TemplateView
from .mixins import AdminTemplateMixin, LoginRequiredMixin


class Dashboard(AdminTemplateMixin, LoginRequiredMixin, TemplateView):
    admin = None
    template_name = 'dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Dashboard, self).get_context_data(*args, **kwargs)
        counters = []
        for model_class in self.admin.site._registry.keys():
            name = model_class._meta.verbose_name_plural
            value = model_class.objects.count()
            counters.append({'name': name, 'value': value})
        context['counters'] = counters
        return context
