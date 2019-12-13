from django.shortcuts import reverse, redirect
from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView
from django.views.generic import UpdateView
from django.utils.translation import ugettext_lazy as _
from .mixins import FormMixin, AdminTemplateMixin, LoginRequiredMixin


class PasswordChange(LoginRequiredMixin, AdminTemplateMixin, FormMixin,
                     FormView):
    admin = None
    template_name = 'password_change.html'
    success_message = _('%(_verbose_name)s password changed')

    def get_form_class(self):
        from django.contrib.auth.forms import PasswordChangeForm
        return PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super(PasswordChange, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return  redirect(reverse(self.admin.urls['logout']))


class PasswordReset(LoginRequiredMixin, AdminTemplateMixin, FormMixin,
                    UpdateView):
    admin = None
    template_name = 'password_change.html'
    success_message = _('%(_verbose_name)s password changed')

    def get_form_class(self):
        from django.contrib.auth.forms import AdminPasswordChangeForm
        return AdminPasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super(PasswordReset, self).get_form_kwargs()
        kwargs['user'] = kwargs.pop('instance')
        return kwargs

    def get_queryset(self):
        return get_user_model()._default_manager.all()
