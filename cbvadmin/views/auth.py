from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView)
from .mixins import AdminMixin


class AdminPasswordResetView(AdminMixin, PasswordResetView):
    success_url = reverse_lazy('cbvadmin:password_reset_done')
    email_template_name = 'cbvadmin/semantic-ui/registration/password_reset_email.html'


class AdminPasswordResetDoneView(AdminMixin, PasswordResetDoneView):
    pass


class AdminPasswordResetConfirmView(AdminMixin, PasswordResetConfirmView):
    success_url = reverse_lazy('cbvadmin:password_reset_complete')


class AdminPasswordResetCompleteView(AdminMixin, PasswordResetCompleteView):
    pass
