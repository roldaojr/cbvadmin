from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from .mixins import (FormMixin, SuccessMixin, AdminMixin,
                     PermissionRequiredMixin)

__all__ = ['EditView', 'AddView', 'DeleteView']


class EditView(PermissionRequiredMixin, AdminMixin, FormMixin,
               UpdateView):
    template_name = 'change_form.html'
    success_message = _('The {name} \"{obj}\" was changed successfully.')


class AddView(PermissionRequiredMixin, AdminMixin, FormMixin, CreateView):
    template_name = 'change_form.html'
    success_message = _('The {name} \"{obj}\" was added successfully.')


class DeleteView(PermissionRequiredMixin, AdminMixin, SuccessMixin,
                 DeleteView):
    template_name = 'delete_confirm.html'
    success_message = _("The %(name)s \"%(obj)s\" was deleted successfully.")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        values = {'name': self.model._meta.verbose_name.title(),
                   'obj': self.object}
        messages.success(self.request, self.success_message % values)
        return response
