from django.test import TestCase
from django.views.generic import View
from django.urls import path
from cbvadmin.actions import Action
from cbvadmin.options import SimpleAdmin, ModelAdmin
from cbvadmin.sites import AdminSite


class SingleActionAdmin(SimpleAdmin):
    actions = {
        'do': Action(View),
        'aonther_do': Action(View, default=True)
    }


class AdminTestCase(TestCase):
    def test_simple_admin(self):
        admin = SingleActionAdmin(site=AdminSite(), namespace='singleaction')
        self.assertEqual(admin.get_path_prefix(), 'singleaction/')
        self.assertEqual(admin.get_url_name(), 'cbvadmin:singleaction')
        self.assertEqual(
            admin.bound_actions['do'].url_name, 'cbvadmin:singleaction:do')

    def test_admin_site_url(self):
        site = AdminSite()
        site.register('singleaction', SingleActionAdmin)
        sitepath = path('cbvadmin/', site.urls)
        sitepath.resolve('cbvadmin/singleaction/do')
        sitepath.resolve('cbvadmin/singleaction/')


class ModeAdminTestCase(TestCase):
    def test_model_admin(self):
        from django.contrib.auth.models import User
        admin = ModelAdmin(site=AdminSite(), model_class=User)
        self.assertEqual(admin.get_path_prefix(), 'auth/user/')
        self.assertEqual(admin.get_url_name(), 'cbvadmin:auth_user')
        for action in ['list', 'add', 'change', 'delete']:
            self.assertEqual(
                admin.bound_actions[action].url_name,
                'cbvadmin:auth_user:%s' % action)

    def test_admin_site_url(self):
        from django.contrib.auth.models import Group
        Group.objects.create(name='g1')
        site = AdminSite()
        site.register(Group, ModelAdmin)
        sitepath = path('cbvadmin/', site.urls)
        sitepath.resolve('cbvadmin/auth/group/')
        sitepath.resolve('cbvadmin/auth/group/add')
        sitepath.resolve('cbvadmin/auth/group/1')
        sitepath.resolve('cbvadmin/auth/group/1/delete')
