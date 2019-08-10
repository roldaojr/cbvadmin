from django.views.generic.list import DetailView as BaseDetailView
from .mixins import AdminMixin, PermissionRequiredMixin


class DetailView(PermissionRequiredMixin, AdminMixin, BaseDetailView):
    detail_fields = None

    def get_context_data(self, **kwargs):
        detail = []
        self.object = self.get_object()

        if self.detail_fields:
            fields = [f for f in type(self.object)._meta.fields
                      if f in self.detail_fields]
        else:
            fields = [f for f in type(self.object)._meta.fields]

        for field in fields:
            detail.append({
                'field': field,
                'value': getattr(self.object, field.name),
                'label': field.verbose_name
            })
        return super().get_context_data(detail=detail, **kwargs)
