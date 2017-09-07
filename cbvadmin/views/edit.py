from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext_lazy as _
from .mixins import (FormMixin, SuccessMixin, AdminMixin,
                     PermissionRequiredMixin)

__all__ = ['EditView', 'AddView', 'DeleteView']


class EditView(PermissionRequiredMixin, AdminMixin, FormMixin,
               UpdateView):
    default_template = 'change_form.html'
    success_message = _('%(_verbose_name)s saved')


class AddView(PermissionRequiredMixin, AdminMixin, FormMixin, CreateView):
    default_template = 'change_form.html'
    success_message = _('%(_verbose_name)s added')


class DeleteView(PermissionRequiredMixin, AdminMixin, SuccessMixin,
                 DeleteView):
    default_template = 'delete_confirm.html'
    success_message = _('%(_verbose_name)s deleted')
