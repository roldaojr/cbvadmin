from django.urls import reverse_lazy
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView)
from .mixins import AdminTemplateMixin


class AdminLoginView(AdminTemplateMixin, LoginView):
    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse_lazy('cbvadmin:dashboard')


class AdminLogoutView(AdminTemplateMixin, LogoutView):
    next_page = reverse_lazy('cbvadmin:login')


class AdminPasswordResetView(AdminTemplateMixin, PasswordResetView):
    success_url = reverse_lazy('cbvadmin:password_reset_done')
    email_template_name = 'cbvadmin/semantic-ui/registration/password_reset_email.html'


class AdminPasswordResetDoneView(AdminTemplateMixin, PasswordResetDoneView):
    pass


class AdminPasswordResetConfirmView(AdminTemplateMixin,
                                    PasswordResetConfirmView):
    success_url = reverse_lazy('cbvadmin:password_reset_complete')


class AdminPasswordResetCompleteView(AdminTemplateMixin,
                                     PasswordResetCompleteView):
    pass
