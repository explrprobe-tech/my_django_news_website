from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

class AuthTest(TestCase):
    "Tests for auth in app News"
    def setUp(self):
        self.User = get_user_model()
        self.admin_user = self.User.objects.create_user(username='admin_user', password='Admin123!')
        self.admin_group, _ = Group.objects.get_or_create(name='Администраторы')
        self.admin_user.groups.add(self.admin_group)
        self.admin_user_login = self.client.login(username='admin_user', password='Admin123!')
        self.admin_user_response = self.client.get(reverse('secret_page'))
        self.regular_user = self.User.objects.create_user(username='regular_user', password='Regular123!')
        self.regular_user_login = self.client.login(username='regular_user', password='Regular123!')
        self.regular_user_response = self.client.get(reverse('secret_page'))
    def test_secret_page_requires_only_admin(self):
        "Test: secret page are required only by admin"
        self.assertTrue(self.admin_user_login, 'Admin was not log in')
        self.assertEqual(self.admin_user_response.status_code, 200, 'Admin can not open secret_page')
        self.assertEqual(self.regular_user_response.status_code, 403, 'Regular user should get 403 on secret_page')
    def test_user_gets_defaut_group(self):
        self.assertTrue(self.regular_user.groups.filter(name='Обычные пользователи').exists(), 'Regular user does not get default group')
    def test_news_creation_permission(self):
        pass