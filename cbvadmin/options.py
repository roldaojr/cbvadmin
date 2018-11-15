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
    menu_weight = 50
    menu_icon = None

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_view_class(self, action):
        view_class = getattr(self, '%s_view_class' % action)
        if view_class is not None:
            view_class.action = None
            view_class.admin = None
        return view_class

    def get_view_kwargs(self, action):
        return {'action': action, 'admin': self}

    def get_view(self, action):
        view_class = self.get_view_class(action)
        view_kwargs = self.get_view_kwargs(action)
        return view_class.as_view(**view_kwargs)

    def get_path_prefix(self):
        return '%s/' % self.namespace

    def get_url_namespace(self):
        return '%s:%s' % (self.site.namespace, self.namespace)

    def _process_actions(self, actions):
        _actions = []
        for name, action_class in actions.items():
            url_namespace = self.get_url_namespace(name)
            action = action_class(
                name=name,
                view=self.get_view(name),
                url_name='%s:%s' % (url_namespace, name)
            )
            _actions[name] = action
            if action.name == self.default_object_action:
                _actions['default_object'] = action
            if action.name == self.default_action:
                _actions['default'] = action
        return _actions

    def get_paths(self):
        return [a.as_path() for a in self.actions.values()]

    def get_menu(self):
        return []

    def has_permission(self, request, action, obj=None):
        return None

    @cached_property
    def actions(self):
        _actions = self._process_actions(self.get_actions())
        return _actions


class SimpleAdmin(BaseAdmin):
    pass


class ModelAdmin(BaseAdmin):
    default_action = 'list'
    default_object_action = 'change'
    model_class = None
    # list related options
    list_display = None
    list_display_links = None
    filterset_class = None
    filter_fields = None
    list_view_class = ListView
    # Add/Edit/Deltee options
    add_view_class = AddView
    edit_view_class = EditView
    delete_view_class = DeleteView
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
            'list': Action,
            'add': Action,
            'change': ObjectAction,
            'delete': ObjectAction
        }

    def get_path_prefix(self):
        return '%s/%s' % (
            self.model_class._meta.app_label,
            self.model_class._meta.model_name)

    def get_menu(self):
        default_action = self.actions['default']
        default_permission = partial(self.has_permission, default_action.name)
        return [MenuItem(self.model_class._meta.verbose_name_plural.title(),
                         reverse(default_action.url_name),
                         check=default_permission,
                         parent=self.model_class._meta.app_label,
                         weight=self.menu_weight,
                         icon=self.menu_icon)]

    def get_success_url(self, *args, **kwargs):
        return reverse(self.actions['default'].url_name)


'''class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'active')
    passwordreset_view_class = PasswordReset

    def get_actions(self):
        actions = super(UserAdmin, self).get_actions()
        actions['passwordreset'] = 'object'
        return actions

    def get_view_kwargs(self, action):
        """Return the view class custom kwargs to create view."""
        if action == 'edit':
            return {'default_template': 'edit_user.html'}
        return {}

    def get_form_class(self, request, obj=None, **kwargs):
        if obj:
            from .forms import UserForm
            return UserForm
        else:
            from django.contrib.auth.forms import UserCreationForm
            return UserCreationForm


class GroupAdmin(ModelAdmin):
    list_display = ('name',)

    def get_form_class(self, request, obj=None, **kwargs):
        from .forms import GroupForm
        return GroupForm
'''
