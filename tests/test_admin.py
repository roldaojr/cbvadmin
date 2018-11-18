from django.test import TestCase
from django.views.generic import View
from django.urls import path
from cbvadmin.actions import Action
from cbvadmin.options import SimpleAdmin, ModelAdmin
from cbvadmin.sites import AdminSite


class SingleActionAdmin(SimpleAdmin):
    do_view_class = View
    aonther_do_view_class = View
    default_action = 'aonther_do'

    def get_actions(self):
        return {
            'do': Action,
            'aonther_do': Action
        }


class AdminTestCase(TestCase):
    def test_simple_admin(self):
        admin = SingleActionAdmin(site=AdminSite(), namespace='singleaction')
        self.assertEqual(admin.get_path_prefix(), 'singleaction/')
        self.assertEqual(admin.get_url_namespace(), 'cbvadmin:singleaction')
        self.assertEqual(
            admin.actions['do'].url_name, 'cbvadmin:singleaction_do')

    def test_admin_site_url(self):
        site = AdminSite()
        site.register('singleaction', SingleActionAdmin)
        sitepath = path('cbvadmin/', site.urls)
        sitepath.resolve('cbvadmin/singleaction/do/')
        sitepath.resolve('cbvadmin/singleaction/')


class ModeAdminTestCase(TestCase):
    def test_model_admin(self):
        from django.contrib.auth.models import User
        admin = ModelAdmin(site=AdminSite(), namespace=User)
        self.assertEqual(admin.get_path_prefix(), 'auth/user/')
        self.assertEqual(admin.get_url_namespace(), 'cbvadmin:auth_user')
        for action in ['list', 'add', 'change', 'delete']:
            self.assertEqual(
                admin.actions[action].url_name,
                'cbvadmin:auth_user_%s' % action)

    def test_admin_site_url(self):
        from django.contrib.auth.models import Group
        Group.objects.create(name='g1')
        site = AdminSite()
        site.register(Group, ModelAdmin)
        sitepath = path('cbvadmin/', site.urls)
        sitepath.resolve('cbvadmin/auth/group/')
        sitepath.resolve('cbvadmin/auth/group/add/')
        sitepath.resolve('cbvadmin/auth/group/1/')
        sitepath.resolve('cbvadmin/auth/group/1/delete/')
