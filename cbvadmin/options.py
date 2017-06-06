from collections import namedtuple
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.utils.functional import cached_property
from django_tables2 import tables
from django_tables2.utils import A
from menu import MenuItem
from .views.list import ListView
from .views.edit import AddView, EditView, DeleteView


def table_factory(model, fields=None, action='edit'):
    linkcol = fields[0] if fields else 'id'
    view_tuple = (model._meta.app_label, model._meta.model_name, action)
    meta_attrs = {'model': model, 'fields': fields}
    attrs = {
        linkcol: tables.columns.LinkColumn('cbvadmin:%s_%s_%s' % view_tuple,
                                           args=[A('pk')]),
        'Meta': type('Meta', (object,), meta_attrs)
    }
    return type('%sTable' % model._meta.object_name,
                (tables.Table,), attrs)


class BaseAdmin(object):
    site = None

    def __init__(self, *args, **kwargs):
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])


AdminAction = namedtuple('AdminAction', ['name', 'target', 'default'])


class ModelAdmin(BaseAdmin):
    default_action = 'list'
    default_object_action = 'edit'
    # list related options
    list_display = None
    list_display_links = None
    list_view_class = ListView
    filterset_class = None
    filter_fields = None
    # Add/Edit/Delte options
    add_view_class = AddView
    edit_view_class = EditView
    delete_view_class = DeleteView
    form_class = None
    # menu item optionns
    menu_weight = 50

    def __init__(self, model_class):
        self.model_class = model_class
        self.model_opts = model_class._meta

    def has_permission(self, action, obj=None):
        return True

    def get_view_class(self, action):
        view_class = getattr(self, '%s_view_class' % action, None)
        if view_class and not hasattr(view_class, 'admin'):
            view_class.admin = None
        return view_class

    def get_table_class(self):
        return table_factory(self.model_class, self.list_display)

    def get_form_class(self, request, obj=None, **kwargs):
        """Return the form class to use."""
        return self.form_class

    def get_actions(self):
        return [
            AdminAction('edit', 'object', True),
            AdminAction('delete', 'object', False),
            AdminAction('list', 'collection', True),
            AdminAction('add', 'collection', False)
        ]

    def get_urls(self):
        app = self.model_class._meta.app_label
        model = self.model_class._meta.model_name
        view_kwargs = {'model': self.model_class, 'admin': self}
        urls = []
        # get valid actions
        actions = self.get_actions()

        for action in actions:
            if action.name == self.default_action:
                pattern = r'^$'
            elif action.name == self.default_object_action:
                pattern = r'^(?P<pk>\d+)/$'
            elif action.target == 'object':
                pattern = r'^(?P<pk>\d+)/%s$' % action.name
            else:
                pattern = r'^%s$' % action.name

            view_class = self.get_view_class(action.name)
            urls.append(url(pattern, view_class.as_view(**view_kwargs),
                            name='%s_%s_%s' % (app, model, action.name)))
        return urls

    @cached_property
    def urls(self):
        app = self.model_class._meta.app_label
        model = self.model_class._meta.model_name
        urls = {a.name: 'cbvadmin:%s_%s_%s' % (app, model, a.name)
                for a in self.get_actions()}
        urls['default'] = 'cbvadmin:%s_%s_%s' % (
            app, model, self.default_action)
        urls['default_object'] = 'cbvadmin:%s_%s_%s' % (
            app, model, self.default_object_action)
        return urls

    def get_menu(self):
        return [MenuItem(self.model_class._meta.verbose_name.title(),
                         reverse(self.urls['default']),
                         weight=self.menu_weight)]

    def get_success_url(self):
        return reverse(self.urls['default'])
