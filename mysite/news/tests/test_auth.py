from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

class AuthTest(TestCase):
    "Tests for auth in app News"
    def setUp(self):
        self.User = get_user_model()
    def test_secret_page_requires_only_admin(self):
        "Test: secret page are required only by admin"
        admin_user = self.User.objects.create_user(
            username='admin_user',
            password='Admin123!'
        )
        admin_group, created = Group.objects.get_or_create(name='Администраторы')
        admin_user.groups.add(admin_group)
        admin_user_login = self.client.login(username='admin_user', password='Admin123!')
        self.assertTrue(admin_user_login, 'Admin was not log in')
        admin_user_response = self.client.get(reverse('secret_page'))
        self.assertEqual(admin_user_response.status_code, 200, 'Admin can not open secret_page')
        regular_user = self.User.objects.create_user(username='regular_user', password='Regular123!')
        regular_user_login = self.client.login(username='regular_user', password='Regular123!')
        regular_user_response = self.client.get(reverse('secret_page'))
        self.assertEqual(regular_user_response.status_code, 403, 'Regular user should get 403 on secret_page')
    def test_user_gets_defaut_group(self):
        pass
    def test_news_creation_permission(self):
        pass