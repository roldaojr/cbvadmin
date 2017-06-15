from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext_lazy as _
from .mixins import (AdminTemplateMixin, FormMixin, SuccessUrlMixin,
                     SuccessMessageMixin)

__all__ = ['EditView', 'AddView', 'DeleteView']


class EditView(AdminTemplateMixin, FormMixin, SuccessUrlMixin,
               SuccessMessageMixin, UpdateView):
    template_name = 'change_form.html'
    fields = '__all__'
    success_message = _('%(_verbose_name)s saved')


class AddView(AdminTemplateMixin, FormMixin, SuccessUrlMixin,
              SuccessMessageMixin, CreateView):
    template_name = 'change_form.html'
    fields = '__all__'
    success_message = _('%(_verbose_name)s added')


class DeleteView(AdminTemplateMixin, SuccessUrlMixin, SuccessMessageMixin,
                 DeleteView):
    template_name = 'delete_confirm.html'
    success_message = _('%(_verbose_name)s deleted')
