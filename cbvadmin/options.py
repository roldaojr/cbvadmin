from django.core.urlresolvers import reverse
from django.conf.urls import url
from django_tables2 import tables
from django_tables2.utils import A
from menu import MenuItem
from .views.list import ListView
from .views.edit import AddView, EditView, DeleteView


def table_factory(model, fields=None):
    linkcol = fields[0] if fields else 'id'
    model_name = (model._meta.app_label, model._meta.model_name)
    meta_attrs = {'model': model, 'fields': fields}
    attrs = {
        linkcol: tables.columns.LinkColumn('cbvadmin:%s_%s_edit' % model_name,
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


class ModelAdmin(BaseAdmin):
    default_action = 'list'
    # list related options
    list_display = None
    list_display_links = None
    list_view_class = ListView
    filterset_class = None
    filter_fields = None
    # Edit related options
    add_view_class = AddView
    edit_view_class = EditView
    delete_view_class = DeleteView
    form_class = None

    def __init__(self, model_class):
        self.model_class = model_class
        self.model_opts = model_class._meta

    def has_permission(self, action, obj=None):
        return True

    def get_view_class(self, action):
        view_class = getattr(self, '%s_view_class' % action)
        if not hasattr(view_class, 'admin'):
            view_class.admin = None
        return view_class

    def get_table_class(self):
        return table_factory(self.model_class, self.list_display)

    def get_form_class(self, request, obj=None, **kwargs):
        """Return the form class to use."""
        return self.form_class

    def get_urls(self):
        app = self.model_class._meta.app_label
        model = self.model_class._meta.model_name
        view_kwargs = {
            'model': self.model_class,
            'admin': self
        }
        object_actions = ('edit', 'delete')
        collection_actions = ('list', 'add')
        urls = []
        for i, action in enumerate(collection_actions):
            pattern = r'^%s$' % action if i > 0 else r'^$'
            urls.append(url(pattern,
                        self.get_view_class(action).as_view(**view_kwargs),
                        name='%s_%s_%s' % (app, model, action)))
        for i, action in enumerate(object_actions):
            pattern = '/%s' % action if i > 0 else ''
            urls.append(url(r'^(?P<pk>\d+)%s$' % pattern,
                            self.get_view_class(action).as_view(**view_kwargs),
                            name='%s_%s_%s' % (app, model, action)))

        return urls

    def get_context_data(self):
        model_name = (self.model_class._meta.app_label,
                      self.model_class._meta.model_name)
        return {
            'model_opts': self.model_class._meta,
            'urls': {
                'list': 'cbvadmin:%s_%s_list' % model_name,
                'add': 'cbvadmin:%s_%s_add' % model_name,
                'edit': 'cbvadmin:%s_%s_edit' % model_name,
                'delete': 'cbvadmin:%s_%s_delete' % model_name,
            }
        }

    def get_menu_item(self):
        view_name = 'cbvadmin:%s_%s_%s' % (self.model_class._meta.app_label,
                                           self.model_class._meta.model_name,
                                           self.default_action)
        return MenuItem(self.model_class._meta.verbose_name.title(),
                        reverse(view_name))
