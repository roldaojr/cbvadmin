from django.contrib.auth.models import User, Permission
from django.urls import reverse
from django.test import TestCase


class StaffUserTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='user', password='user')
        User.objects.create_user(username='staff', password='staff',
                                 is_staff=True)

    def test_dashboard_annonymous(self):
        url = reverse('cbvadmin:dashboard')
        resp = self.client.get(url)
        self.assertRedirects(
            resp, '%s?next=%s' % (reverse('cbvadmin:login'), url))

    def test_dashboard_user(self):
        self.client.login(username='user', password='user')
        url = reverse('cbvadmin:dashboard')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_dashboard_staff_user(self):
        self.client.login(username='staff', password='staff')
        url = reverse('cbvadmin:dashboard')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


class PermissionTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='user', password='user')
        perms_map = {'list': 'change', 'edit': 'change'}
        for action in ('list', 'edit', 'add', 'delete'):
            user = User.objects.create_user(username='user_%s' % action,
                                            password='user_%s' % action)
            codename = '%s_user' % perms_map.get(action, action)
            perm = Permission.objects.get(content_type__app_label='auth',
                                          codename=codename)
            user.user_permissions.add(perm)

    def test_admin_list_allowed(self):
        self.client.login(username='user_list', password='user_list')
        url = reverse('cbvadmin:auth_user_list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_admin_list_denied(self):
        self.client.login(username='user', password='user')
        url = reverse('cbvadmin:auth_user_list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)

    def test_admin_add_allowed(self):
        self.client.login(username='user_add', password='user_add')
        url = reverse('cbvadmin:auth_user_add')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_user_add_denied(self):
        self.client.login(username='user', password='user')
        url = reverse('cbvadmin:auth_user_add')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)

    def test_admin_edit_allowed(self):
        self.client.login(username='user_edit', password='user_edit')
        url = reverse('cbvadmin:auth_user_edit', kwargs={'pk': 1})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_user_edit_denied(self):
        self.client.login(username='user', password='user')
        url = reverse('cbvadmin:auth_user_edit', kwargs={'pk': 1})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)

    def test_admin_delete_allowed(self):
        self.client.login(username='user_delete', password='user_delete')
        url = reverse('cbvadmin:auth_user_delete', kwargs={'pk': 1})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_user_delete_denied(self):
        self.client.login(username='user', password='user')
        url = reverse('cbvadmin:auth_user_delete', kwargs={'pk': 1})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)
