import pytest
from django.test import TestCase
from cbvadmin import site


@pytest.mark.django_db
class AdminActionsTestCase(TestCase):
    def test_get_urls(self):
        for model, admin in site._registry.items():
            print(admin.get_urls())
