from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.messages.views import (
    SuccessMessageMixin as SuccessMessageMixin_)
from django.utils.functional import cached_property
from django_filters import CharFilter
from django_filters.filterset import FilterSet
from django_filters.views import FilterMixin
from crispy_forms.helper import FormHelper


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


class ViewMixin(object):
    admin = None

    def get_context_data(self, **kwargs):
        context = super(ViewMixin, self).get_context_data(**kwargs)
        if self.admin and hasattr(self.admin, 'get_context_data'):
            context['admin'] = self.admin.get_context_data()
        return context


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
    def get_form_class(self):
        form_class = self.admin.get_form_class(self.request, self.object)
        if form_class is None:
            form_class = super(FormMixin, self).get_form_class()
        return form_class

    def get_form(self, form_class=None):
        form = super(FormMixin, self).get_form(form_class)
        if not hasattr(form, 'helper'):
            form.helper = FormHelper()
        form.helper.form_id = 'change_form'
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
        model_name = (self.model._meta.app_label,
                      self.model._meta.object_name.lower())
        return reverse('cbvadmin:%s_%s_list' % model_name)
