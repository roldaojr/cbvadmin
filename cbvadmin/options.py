from copy import copy
from django.urls import path, reverse, reverse_lazy
from django.utils.functional import cached_property
from menu import MenuItem
from .actions import Action, BoundAction
from .tables import table_factory
from .views.edit import AddView, EditView, DeleteView
from .views.list import ListView


class BaseAdmin(object):
    site = None
    namespace = None
    default_action = None
    default_object_action = None
    permissions = {}
    menu_weight = 50
    menu_icon = None
    actions = {}

    def __init__(self, namespace, *args, **kwargs):
        self.namespace = namespace
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.bound_actions = {}
        self._bound_actions()

    def _bound_actions(self):
        for name, action in self.actions.items():
            if action.view_class is not None:
                view_kwargs = self.get_view_kwargs(action)
                for attr in view_kwargs:
                    if not hasattr(action.view_class, attr):
                        setattr(action.view_class, attr, None)
                view_func = action.view_class.as_view(**view_kwargs)
                self.bound_actions[name] = BoundAction(
                    self, name=name, view=view_func,
                    default=action.default, item=action.item, path=action.path)
            else:
                raise ValueError('view_class for action "%s" is undefined (namespace %s).' % (name, self.namespace))

    def get_view_kwargs(self, action):
        return {'action': action, 'admin': self}

    def get_path_prefix(self):
        return '%s/' % self.namespace if self.namespace else ''

    def get_permisson(self, action, **kwargs):
        return self.permissions.get(action, None)

    def has_permission(self, request, action):
        return True

    def get_url_name(self, action=None):
        namespace = [self.site.namespace]
        if self.namespace:
            namespace.append(self.namespace)
        if action:
            namespace.append(action)
        return ':'.join(namespace)

    def get_urls(self):
        urls = []
        for action in self.bound_actions.values():
            if action.item:
                action_path = ['<int:pk>']
            else:
                action_path = []
            if not action.default:
                action_path.append(action.name)
            urls.append(path('/'.join(action_path), action.view,
                             name=action.name))

        if self.namespace:
            return urls, self.namespace
        else:
            return urls

    def get_menu(self):
        return []

    def get_default_action(self, item=False):
        actions = [
            action for action in self.bound_actions.values()
            if action.default and action.item is item
        ]
        if len(actions) < 1:
            raise ValueError('%s must have a default action' % type(self))
        if len(actions) > 1:
            raise ValueError('%s must have only one default action' % type(self))
        return actions[0]


    @cached_property
    def urls(self):
        admin_urls = {}
        for name, action in self.bound_actions.items():
            admin_urls[name] = self.get_url_name(action.name)
            if action.default:
                if action.item:
                    admin_urls['default_object'] = self.get_url_name(action.name)
                else:
                    admin_urls['default'] = self.get_url_name(action.name)
        return admin_urls


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
    basic_actions = ['list', 'add', 'change', 'delete']

    def __init__(self, model_class, *args, **kwargs):
        self.model_class = model_class
        self.model_opts = model_class._meta
        namespace = '%s_%s' % (
            self.model_class._meta.app_label,
            self.model_class._meta.model_name)
        super().__init__(namespace, *args, **kwargs)

    def get_table_class(self):
        item_action = self.get_default_action(item=True)
        return table_factory(self.model_class, self.list_display,
                             action=item_action.url_name)

    def get_form_class(self, request, obj=None, **kwargs):
        return self.form_class

    def get_view_kwargs(self, action):
        kwargs = super().get_view_kwargs(action)
        kwargs.update({'model': self.model_class})
        return kwargs

    def _bound_actions(self):
        model_actions = {
            'list': Action(ListView, perm='view', default=True),
            'add': Action(AddView, perm='add'),
            'change': Action(EditView, perm='change', item=True, default=True),
            'delete': Action(DeleteView, perm='delete', item=True)
        }
        for name, action in model_actions.items():
            if name not in self.actions and name in self.basic_actions:
                self.actions[name] = action
        super()._bound_actions()

    def get_path_prefix(self):
        return '%s/%s/' % (
            self.model_class._meta.app_label,
            self.model_class._meta.model_name)

    def get_permisson(self, action):
        action_perm = getattr(action, 'perm', action)
        default_perm = '%s.%s_%s' % (
            self.model_class._meta.app_label, action_perm,
            self.model_class._meta.model_name)
        return self.permissions.get(action, default_perm)

    def has_permission(self, request, action, obj=None, **kwargs):
        return request.user.has_perm(self.get_permisson(action))

    def get_menu(self):
        default_action = self.get_default_action()
        return [MenuItem(self.model_class._meta.verbose_name_plural.title(),
                         reverse(self.get_url_name(default_action.name)),
                         check=lambda r: self.has_permission(r, default_action),
                         parent=self.model_class._meta.app_label,
                         weight=self.menu_weight,
                         icon=self.menu_icon)]

    def get_success_url(self, *args, **kwargs):
        action = self.get_default_action()
        return reverse(self.urls[action.name])
