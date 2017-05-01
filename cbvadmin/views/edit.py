
from django.views.generic import (CreateView, UpdateView,
                                  DeleteView as DeleteView_)
from django.utils.translation import ugettext_lazy as _
from .mixins import (ViewMixin, FormMixin, SuccessUrlMixin, SuccessMessageMixin)

__all__ = ['EditView', 'AddView', 'DeleteView']


class EditView(ViewMixin, FormMixin, SuccessUrlMixin,
               SuccessMessageMixin, UpdateView):
    template_name = 'change_form.html'
    fields = '__all__'
    success_message = _('%(_verbose_name)s saved')


class AddView(ViewMixin, FormMixin, SuccessUrlMixin,
              SuccessMessageMixin, CreateView):
    template_name = 'change_form.html'
    fields = '__all__'
    success_message = _('%(_verbose_name)s added')


class DeleteView(ViewMixin, SuccessUrlMixin, SuccessMessageMixin,
                 DeleteView_):
    template_name = 'delete_confirm.html'
    success_message = _('%(_verbose_name)s deleted')
