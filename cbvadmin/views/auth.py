from django.urls import reverse_lazy
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView)
from .mixins import AdminTemplateMixin


class AdminLoginView(AdminTemplateMixin, LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse_lazy('cbvadmin:dashboard')


class AdminLogoutView(AdminTemplateMixin, LogoutView):
    next_page = reverse_lazy('cbvadmin:accounts:login')


class AdminPasswordResetView(AdminTemplateMixin, PasswordResetView):
    email_template_name = 'cbvadmin/registration/password_reset_email.html'

    def get_success_url(self):
        return reverse_lazy(self.admin.urls['password_reset_done'])


class AdminPasswordResetDoneView(AdminTemplateMixin, PasswordResetDoneView):
    pass


class AdminPasswordResetConfirmView(AdminTemplateMixin,
                                    PasswordResetConfirmView):
    def get_success_url(self):
        return reverse_lazy(self.admin.urls['password_reset_complete'])


class AdminPasswordResetCompleteView(AdminTemplateMixin,
                                     PasswordResetCompleteView):
    pass
