from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext_lazy as _
from .mixins import AdminTemplateMixin, FormMixin, SuccessMixin

__all__ = ['EditView', 'AddView', 'DeleteView']


class EditView(AdminTemplateMixin, FormMixin, UpdateView):
    default_template = 'change_form.html'
    success_message = _('%(_verbose_name)s saved')


class AddView(AdminTemplateMixin, FormMixin, CreateView):
    default_template = 'change_form.html'
    success_message = _('%(_verbose_name)s added')


class DeleteView(AdminTemplateMixin, SuccessMixin, DeleteView):
    default_template = 'delete_confirm.html'
    success_message = _('%(_verbose_name)s deleted')
