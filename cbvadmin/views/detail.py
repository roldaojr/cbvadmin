from django.views.generic.detail import DetailView as BaseDetailView
from .mixins import AdminMixin, PermissionRequiredMixin


class DetailView(PermissionRequiredMixin, AdminMixin, BaseDetailView):
    pass
