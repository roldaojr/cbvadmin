from django.views.generic.edit import FormView
from .mixins import FormMixin, AdminTemplateMixin, LoginRequiredMixin


class PasswordChange(LoginRequiredMixin, AdminTemplateMixin, FormMixin,
                     FormView):
    admin = None
    template_name = 'password_change.html'

    def get_form_class(self):
        from django.contrib.auth.forms import PasswordChangeForm
        return PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super(PasswordChange, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
