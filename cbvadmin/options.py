from functools import partial
from django.urls import reverse
from django.utils.functional import cached_property
from menu import MenuItem
from .actions import Action, ObjectAction
from .tables import table_factory
from .views.edit import AddView, EditView, DeleteView
from .views.list import ListView


class BaseAdmin(object):
    site = None
    namespace = None
    default_action = None
    default_object_action = None
    view_classes = {}
    permissions = {}
    menu_weight = 50
    menu_icon = None

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_view_class(self, action):
        view_class = self.view_classes.get(action.name, action.view_class)
        if view_class is not None:
            view_class.action = None
            view_class.admin = None
        return view_class

    def get_view_kwargs(self, action):
        return {'action': action, 'admin': self}

    def get_path_prefix(self):
        return '%s/' % self.namespace

    def get_permisson(self, action, **kwargs):
        return self.permissions.get(action, None)

    def get_url_namespace(self):
        return '%s:%s' % (self.site.namespace, self.namespace)

    def get_actions(self):
        return {}

    @cached_property
    def actions(self):
        _actions = {}
        for name, action in self.get_actions().items():
            action.url_name = '%s_%s' % (self.get_url_namespace(), name)
            action.name = name

            view_class = self.get_view_class(action)
            if view_class is not None:
                view_kwargs = self.get_view_kwargs(action)
                action.view = view_class.as_view(**view_kwargs)
            else:
                raise ValueError('admin action must have a view class.')

            _actions[name] = action

            if name == self.default_object_action:
                action.path = '<int:pk>'
                _actions['default_object'] = action
            elif name == self.default_action:
                action.path = ''
                _actions['default'] = action

        return _actions

    def get_urls(self):
        return [a.as_path() for a in self.actions.values()]

    def get_menu(self):
        return []


class SimpleAdmin(BaseAdmin):
    pass


class ModelAdmin(BaseAdmin):
    default_action = 'list'
    default_object_action = 'change'
    model_class = None
    view_classes = {}
    # list related options
    list_display = None
    list_display_links = None
    filterset_class = None
    filter_fields = None
    form_class = None
    # menu item optionns
    menu_weight = 50
    menu_icon = None

    def __init__(self, *args, **kwargs):
        model_class = kwargs.get('namespace')
        self.model_class = model_class
        self.model_opts = model_class._meta
        kwargs['namespace'] = '%s_%s' % (
            self.model_class._meta.app_label,
            self.model_class._meta.model_name)
        super().__init__(*args, **kwargs)

    def get_table_class(self):
        return table_factory(self.model_class, self.list_display,
                             action=self.default_object_action)

    def get_form_class(self, request, obj=None, **kwargs):
        return self.form_class

    def get_view_kwargs(self, action):
        kwargs = super().get_view_kwargs(action)
        kwargs.update({'model': self.model_class})
        return kwargs

    def get_actions(self):
        return {
            'list': Action(ListView, perm='view'),
            'add': Action(AddView),
            'change': ObjectAction(EditView),
            'delete': ObjectAction(DeleteView)
        }

    def get_path_prefix(self):
        return '%s/%s/' % (
            self.model_class._meta.app_label,
            self.model_class._meta.model_name)

    def get_permisson(self, action):
        action_perm = getattr(action, 'perm', action.name)
        default_perm = '%s.%s_%s' % (
            self.model_class._meta.app_label, action_perm,
            self.model_class._meta.model_name)
        return self.permissions.get(action, default_perm)

    def has_permission(self, request, action, **kwargs):
        return request.user.has_perm(self.get_permisson(action))

    def get_menu(self):
        default_action = self.actions['default']
        default_permission = partial(self.has_permission,
                                     action=default_action)
        return [MenuItem(self.model_class._meta.verbose_name_plural.title(),
                         reverse(default_action.url_name),
                         check=default_permission,
                         parent=self.model_class._meta.app_label,
                         weight=self.menu_weight,
                         icon=self.menu_icon)]

    def get_success_url(self, *args, **kwargs):
        return reverse(self.actions['default'].url_name)
