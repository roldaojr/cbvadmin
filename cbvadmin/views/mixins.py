from django.db import models
from django.urls import reverse
from django.apps import apps
from django.contrib.auth.mixins import (
    AccessMixin,
    LoginRequiredMixin as BaseLoginRequiredMixin,
    PermissionRequiredMixin as BasePermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django_filters import CharFilter
from django_filters.filterset import FilterSet
from django_filters.views import FilterMixin
from crispy_forms.helper import FormHelper
from ..sites import site
from ..utils import get_setting


__all__ = (
    'LoginRequiredMixin', 'AdminTemplateMixin',
    'SuccessMixin', 'FormMixin', 'FilterMixin', 'AccessMixin'
)


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
    model = model._meta.object_name
    filterset = type(f'{model}FilterSet', (FilterSet,), {'Meta': meta})
    return filterset


class LoginRequiredMixin(BaseLoginRequiredMixin):
    def get_login_url(self):
        return reverse('cbvadmin:accounts:login')


class PermissionRequiredMixin(BasePermissionRequiredMixin):
    def has_permission(self):
        if self.admin:
            try:
                obj = self.get_object()
            except AttributeError:
                obj = None
            has_perm = self.admin.has_permission(
                self.request, self.action, obj)
            if has_perm is not None:
                return has_perm

        perms = self.get_permission_required()
        return self.request.user.has_perm(perms)


class AdminTemplateMixin:
    def get_template_names(self, *args, **kwargs):
        template_names = super().get_template_names(*args, **kwargs)
        template_pack = get_setting('TEMPLATE_PACK', 'adminlte3')
        return [
            f'cbvadmin/{template_pack}/{template_name}'
            for template_name in template_names
        ]


class AdminMixin(LoginRequiredMixin, AdminTemplateMixin):
    admin = None
    action = None

    def get_breakcrumbs(self):
        breakcrumbs = []
        if hasattr(self, 'model'):
            app_config = apps.get_app_config(self.model._meta.app_label)
            breakcrumbs.append(app_config.verbose_name)
            breakcrumbs.append(self.model._meta.verbose_name_plural.title()) # NOQA
        elif hasattr(self, 'admin') and hasattr(self.admin, 'namespace'):
            # pylint: disable=protected-access
            if self.admin.namespace in site._registry['menu']: 
                breakcrumbs.append(site._registry['menu'][self.admin.namespace].title)
            else:
                breakcrumbs.append(_(self.admin.namespace.title()))
        if not self.admin.actions[self.action].default or self.admin.actions[self.action].item:
            breakcrumbs.append(_(self.action.title()))
            
        return breakcrumbs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perms = {}
        urls = {}
        for name, action in self.admin.bound_actions.items():
            perms[name] = self.admin.has_permission(self.request, name)
            default_key = 'default_item' if action.item else 'default'
            if action.default:
                perms[default_key] = perms[name]

            if perms[name]:
                urls[name] = self.admin.get_url_name(name)
                if action.default:
                    urls[default_key] = self.admin.get_url_name(name)

        context.update({
            'admin': {'perms': perms, 'urls': urls},
            'breakcrumbs': self.get_breakcrumbs()
        })
        return context


class SuccessMixin(SuccessMessageMixin):
    success_message = None

    def get_success_message(self, cleaned_data):
        if self.success_message:
            return self.success_message.format(
                name=self.model._meta.verbose_name.title(),
                obj=self.object
            )

    def get_success_url(self):
        return self.admin.get_success_url(view=self)


class FormMixin(SuccessMixin):
    form_id = 'change_form'
    fields = None

    def get_form_class(self):
        form_class = self.form_class
        if self.admin and hasattr(self.admin, 'get_form_class'):
            form_class = self.admin.get_form_class(self.request, self.object)
        if form_class is None:
            if self.fields is None:
                self.fields = '__all__'
            form_class = super().get_form_class()
        return form_class

    def get_form_helper(self):
        helper = FormHelper()
        helper.form_id = self.form_id
        helper.form_tag = False
        helper.include_media = False
        return helper

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not hasattr(form, 'helper'):
            form.helper = self.get_form_helper()
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
