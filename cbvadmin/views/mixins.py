from django.db import models
from django.urls import reverse
from django.contrib.auth.mixins import (
    AccessMixin,
    LoginRequiredMixin as _LoginRequiredMixin,
    PermissionRequiredMixin as _PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.functional import cached_property
from django_filters import CharFilter
from django_filters.filterset import FilterSet
from django_filters.views import FilterMixin
from crispy_forms.helper import FormHelper
from ..utils import get_setting


__all__ = ('AccessMixin', 'LoginRequiredMixin', 'AdminTemplateMixin',
           'SuccessMixin', 'FormMixin', 'FilterMixin')


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


class AdminAccessMixin(object):
    def get_login_url(self):
        return reverse('cbvadmin:accounts:login')


class LoginRequiredMixin(AdminAccessMixin, _LoginRequiredMixin):
    pass


class PermissionRequiredMixin(AdminAccessMixin, _PermissionRequiredMixin):
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


class AdminTemplateMixin(object):
    def get_admin_template(self, name):
        template_pack = get_setting('TEMPLATE_PACK')
        return 'cbvadmin/%s/%s' % (template_pack, name)

    def get_template_names(self, *args, **kwargs):
        template_names = super(
            AdminTemplateMixin, self).get_template_names(*args, **kwargs)
        default_template = getattr(self, 'default_template', None)
        if default_template:
            template_names.append(default_template)
        admin_templates = ['cbvadmin/%s' % t for t in
                           reversed(template_names)]
        template_pack = get_setting('TEMPLATE_PACK', '')
        if template_pack:
            ui_templates = ['cbvadmin/%s/%s' % (template_pack, t) for t in
                            reversed(template_names)]
        else:
            ui_templates = []
        return admin_templates + ui_templates


class AdminMixin(LoginRequiredMixin, AdminTemplateMixin):
    admin = None
    action = None

    def get_context_data(self, **kwargs):
        context = super(AdminMixin, self).get_context_data(**kwargs)
        admin_perms = {
            action: self.admin.has_permission(self.request, action)
            for action in self.admin.actions.keys()
        }
        admin_perms.update({
            'default': self.admin.has_permission(
                self.request, self.admin.default_action),
            'default_object': self.admin.has_permission(
                self.request, self.admin.default_object_action)
        })
        admin_urls = {
            action: url
            for action, url in self.admin.urls.items()
            if admin_perms[action]
        }
        context.update({
            'admin': {
                'perms': admin_perms,
                'urls': admin_urls
            }
        })
        return context


class SuccessMixin(SuccessMessageMixin):
    success_message = None

    def get_success_message(self, cleaned_data):
        if self.success_message:
            return self.success_message.format(
                name=self.model._meta.verbose_name.title(),
                obj=self.object)

    def get_success_url(self):
        return self.admin.get_success_url(view=self)


class FormMixin(SuccessMixin):
    form_id = 'change_form'

    def get_form_class(self):
        form_class = self.admin.get_form_class(self.request, self.object)
        if form_class is None:
            if self.form_class is None and self.fields is None:
                self.fields = '__all__'
            form_class = super(FormMixin, self).get_form_class()
        return form_class

    def get_form_helper(self):
        helper = FormHelper()
        helper.form_id = self.form_id
        helper.form_tag = False
        return helper

    def get_form(self, form_class=None):
        form = super(FormMixin, self).get_form(form_class)
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
