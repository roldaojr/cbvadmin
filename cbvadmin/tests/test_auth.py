from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User


class AdminAuthTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='user', password='user')

    def test_already_loggedin_from_login(self):
        ''' Request to login url from logged user must redirect to home '''
        self.client.login(username='user', password='user')
        url = reverse('cbvadmin:login')
        resp = self.client.get(url)
        self.assertRedirects(resp, reverse('cbvadmin:dashboard'))
