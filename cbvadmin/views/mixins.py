import inspect
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.messages.views import (
    SuccessMessageMixin as SuccessMessageMixin_)
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import (HttpResponse, StreamingHttpResponse)
from django.utils.functional import cached_property
from django_filters import CharFilter
from django_filters.filterset import FilterSet
from django_filters.views import FilterMixin
from crispy_forms.helper import FormHelper
from ..utils import get_setting


__all__ = ('ViewMixin', 'FormMixin', 'FilterMixin', 'SuccessUrlMixin')


filter_overrides = {
    models.CharField: {
        'filter_class': CharFilter,
        'extra': lambda f: {
            'lookup_expr': 'icontains',
        },
    }
}


def filterset_factory(model, fields):
    meta = type(str('Meta'), (object,), {
        'model': model, 'fields': fields,
        'filter_overrides': filter_overrides
    })
    filterset = type(str('%sFilterSet' % model._meta.object_name),
                     (FilterSet,), {'Meta': meta})
    return filterset


class AccessMixin(object):
    """
    'Abstract' mixin that gives access mixins the same customizable
    functionality.
    """
    login_url = None
    raise_exception = False
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth
    redirect_unauthenticated_users = False

    def get_login_url(self):
        return reverse('cbvadmin:login')

    def get_redirect_field_name(self):
        """
        Override this method to customize the redirect_field_name.
        """
        if self.redirect_field_name is None:
            raise ImproperlyConfigured(
                '{0} is missing the '
                'redirect_field_name. Define {0}.redirect_field_name or '
                'override {0}.get_redirect_field_name().'.format(
                    self.__class__.__name__))
        return self.redirect_field_name

    def handle_no_permission(self, request):
        if self.raise_exception:
            if (self.redirect_unauthenticated_users and
                    not request.user.is_authenticated):
                return self.no_permissions_fail(request)
            else:
                if (inspect.isclass(self.raise_exception) and
                        issubclass(self.raise_exception, Exception)):
                    raise self.raise_exception
                if callable(self.raise_exception):
                    ret = self.raise_exception(request)
                    if isinstance(ret, (HttpResponse, StreamingHttpResponse)):
                        return ret
                raise PermissionDenied

        return self.no_permissions_fail(request)

    def no_permissions_fail(self, request=None):
        """
        Called when the user has no permissions and no exception was raised.
        This should only return a valid HTTP response.

        By default we redirect to login.
        """
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.get_full_path(),
                                 self.get_login_url(),
                                 self.get_redirect_field_name())


class LoginRequiredMixin(AccessMixin):
    """
    View mixin which verifies that the user is authenticated.

    NOTE:
        This should be the left-most mixin of a view, except when
        combined with CsrfExemptMixin - which in that case should
        be the left-most mixin.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission(request)

        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class ViewMixin(LoginRequiredMixin):
    admin = None

    def get_template_names(self, *args, **kwargs):
        template_names = super(ViewMixin, self).get_template_names(
            *args, **kwargs)
        theme = get_setting('theme', 'materialize')
        return map(lambda t: 'cbvadmin/%s/%s' % (theme, t), template_names)


class SuccessMessageMixin(SuccessMessageMixin_):
    success_message = None

    def get_success_message(self, cleaned_data):
        if self.success_message:
            return self.success_message % dict(
                cleaned_data,
                _verbose_name=self.model._meta.verbose_name.title())
        else:
            return 'Success'


class FormMixin(object):
    form_id = 'change_form'

    def get_form_class(self):
        form_class = self.admin.get_form_class(self.request, self.object)
        if form_class is None:
            form_class = super(FormMixin, self).get_form_class()
        return form_class

    def get_form(self, form_class=None):
        form = super(FormMixin, self).get_form(form_class)
        if not hasattr(form, 'helper'):
            form.helper = FormHelper()
        form.helper.form_id = self.form_id
        return form


class FilterMixin(FilterMixin):
    filterset_class = None
    filter_fields = None

    def get_filter_fields(self):
        if not self.filter_fields:
            if self.admin.filter_fields:
                self.filter_fields = self.admin.filter_fields
        return self.filter_fields

    def get_filterset_class(self):
        if self.filterset_class:
            return self.filterset_class
        if self.admin.filterset_class:
            return self.admin.filterset_class
        filter_fields = self.get_filter_fields()
        if filter_fields and self.model:
            fs = filterset_factory(model=self.model, fields=filter_fields)
            self.filterset_class = fs
            return fs
        return None

    @cached_property
    def filterset(self):
        filterset_class = self.get_filterset_class()
        if filterset_class:
            return self.get_filterset(filterset_class)
        return None

    def has_filters(self):
        return bool(self.filterset)

    def get_context_data(self, **kwargs):
        context = super(FilterMixin, self).get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class SuccessUrlMixin(object):
    def get_success_url(self):
        return self.admin.get_success_url()
