import six
from django.conf.urls import url
from django.contrib.auth import get_permission_codename
from django.core.urlresolvers import reverse
from django.utils.functional import cached_property
from menu import MenuItem
from .tables import table_factory
from .views.edit import AddView, EditView, DeleteView
from .views.list import ListView
from .views.user import PasswordReset


class BaseAdmin(object):
    site = None

    def __init__(self, *args, **kwargs):
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])


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

    def has_permission(self, request, action, obj=None):
        # fix action for permission name
        if action in ('edit', 'list'):
            action = 'change'

        opts = self.model_class._meta
        permission = '%s.%s' % (opts.app_label, get_permission_codename(
            action, opts))
        return request.user.has_perm(permission)

    def get_view_class(self, action):
        view_class = getattr(self, '%s_view_class' % action)
        view_class.action = action
        if view_class and not hasattr(view_class, 'admin'):
            view_class.admin = None
        return view_class

    def get_view_kwargs(self, action):
        """Return the view class custom kwargs to create view."""
        if action == 'edit':
            return {'default_template': 'edit_user.html'}
        return {}

    def get_table_class(self):
        return table_factory(self.model_class, self.list_display,
                             action=self.default_object_action)

    def get_form_class(self, request, obj=None, **kwargs):
        """Return the form class to use."""
        return self.form_class

    def get_actions(self):
        return {
            'edit': 'object',
            'delete': 'object',
            'list': 'collection',
            'add': 'collection'
        }

    def get_urls(self):
        app = self.model_class._meta.app_label
        model = self.model_class._meta.model_name
        urls = []
        # get valid actions
        actions = self.get_actions()

        for action, target in six.iteritems(actions):
            if action == self.default_action:
                pattern = r'^$'
            elif action == self.default_object_action:
                pattern = r'^(?P<pk>\d+)/$'
            elif target == 'object':
                pattern = r'^(?P<pk>\d+)/%s$' % action
            else:
                pattern = r'^%s$' % action

            view_class = self.get_view_class(action)
            view_kwargs = self.get_view_kwargs(action)
            view_kwargs.update({'model': self.model_class, 'admin': self})
            urls.append(url(pattern, view_class.as_view(**view_kwargs),
                            name='%s_%s_%s' % (app, model, action)))
        return urls

    @cached_property
    def urls(self):
        app = self.model_class._meta.app_label
        model = self.model_class._meta.model_name
        urls = {a: 'cbvadmin:%s_%s_%s' % (app, model, a)
                for a, t in six.iteritems(self.get_actions())}
        urls['default'] = 'cbvadmin:%s_%s_%s' % (
            app, model, self.default_action)
        urls['default_object'] = 'cbvadmin:%s_%s_%s' % (
            app, model, self.default_object_action)
        return urls

    def get_menu(self):
        return [MenuItem(self.model_class._meta.verbose_name_plural.title(),
                         reverse(self.urls['default']),
                         weight=self.menu_weight)]

    def get_success_url(self, view):
        return reverse(self.urls['default'])


class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'active')
    passwordreset_view_class = PasswordReset

    def get_actions(self):
        actions = super(UserAdmin, self).get_actions()
        actions['passwordreset'] = 'object'
        return actions

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
