# pylint: disable=protected-access
from django.urls import path, reverse
from menu import MenuItem
from .actions import Action, BoundAction
from .tables import table_factory
from .views.edit import AddView, EditView, DeleteView
from .views.list import ListView


class BaseAdmin:
    site = None
    namespace = None
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
                view_kwargs = self.get_view_kwargs(name)
                for attr in view_kwargs:
                    if not hasattr(action.view_class, attr):
                        setattr(action.view_class, attr, None)
                view_func = action.view_class.as_view(**view_kwargs)
                self.bound_actions[name] = BoundAction(
                    self, name=name, view=view_func, perm=action.perm,
                    default=action.default, item=action.item, path=action.path)
            else:
                raise ValueError(
                    f'view_class for action "{name}" is undefined'
                    '(namespace {self.namespace}).'
                )

    def get_view_kwargs(self, action):
        return {'action': action, 'admin': self}

    def get_path_prefix(self):
        return f'{self.namespace}/' if self.namespace else ''

    def get_permisson(self, action, **kwargs):
        return self.permissions.get(action, None)

    def has_permission(self, *args, **kwargs):
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
            action_path = []
            if action.path:
                action_path.append(action.path)
            else:
                if action.item:
                    action_path.append('<int:pk>')
                if not action.default:
                    action_path.append(action.name)
            urls.append(path('/'.join(action_path), action.view,
                             name=action.name))

        if self.namespace:
            return urls, self.namespace

        return urls

    def get_menu(self):
        return []

    def get_default_action(self, item=False):
        actions = [
            action for action in self.bound_actions.values()
            if action.default and action.item is item
        ]
        if not actions:
            raise ValueError(f'{type(self)} must have a default action')
        if len(actions) > 1:
            raise ValueError(f'{type(self)} must have only one default action')
        return actions[0].name

    @property
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

    @property
    def default_action(self):
        return filter(lambda a: a.default, self.actions.values())

    @property
    def default_item_action(self):
        return filter(lambda a: a.default and a.item, self.actions.values())


class SimpleAdmin(BaseAdmin):
    pass


class ModelAdmin(BaseAdmin):
    model_class = None
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
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        namespace = f'{app_label}_{model_name}'
        super().__init__(namespace, *args, **kwargs)

    def get_table_class(self):
        action_url = self.get_url_name(self.get_default_action(item=True))
        return table_factory(self.model_class, self.list_display,
                             action=action_url)

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
        app_label = self.model_class._meta.app_label
        model_name = self.model_class._meta.model_name
        return f'{app_label}/{model_name}/'

    def get_permisson(self, action):
        action_perm = getattr(self.bound_actions[action], 'perm', None)
        if action_perm:
            app_label = self.model_class._meta.app_label
            model_name = self.model_class._meta.model_name
            default_perm = f'{app_label}.{action_perm}_{model_name}'
            return self.permissions.get(action, default_perm)
        return None

    def has_permission(self, request, action, obj=None, **kwargs):
        perm = self.get_permisson(action)
        return request.user.has_perm(perm) if perm else True

    def get_menu(self):
        default_action = self.get_default_action()
        parent = getattr(self, 'parent_menu', self.model_class._meta.app_label)
        return [
            MenuItem(
                self.model_class._meta.verbose_name_plural.title(),
                reverse(self.get_url_name(default_action)),
                check=lambda r: self.has_permission(r, default_action),
                parent=parent,
                weight=self.menu_weight,
                icon=self.menu_icon
            )
        ]

    def get_success_url(self, *args, **kwargs):
        action = self.get_default_action()
        return reverse(self.urls[action])
