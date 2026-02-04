from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from news.tests.test_base import admin_user, regular_user, create_editor_user

class AuthTest(TestCase):
    "Tests for auth in app News"
    def setUp(self):
        self.admin_user, self.admin_password = admin_user()
        self.regular_user, self.regular_password = regular_user()
        self.editor_user, self.editor_password = create_editor_user()
    def test_secret_page_requires_only_admin(self):
        "Test: secret page are required only by admin"
        self.client.logout()
        anonymous_user_response = self.client.get(reverse('secret_page'))
        self.assertEqual(anonymous_user_response.status_code, 302, 'Anonymous can open secret_page')
        self.assertIn('/login/', anonymous_user_response.url)
        self.client.logout()
        admin_user_login = self.client.login(username=self.admin_user.username, password=self.admin_password)
        admin_user_response = self.client.get(reverse('secret_page'))
        self.assertEqual(admin_user_response.status_code, 200, 'Admin can not open secret_page')
        self.client.logout()
        regular_user_login = self.client.login(username=self.regular_user.username, password=self.regular_password)
        regular_user_response = self.client.get(reverse('secret_page'))
        self.assertEqual(regular_user_response.status_code, 403, 'Regular user should get 403 on secret_page')
    def test_user_gets_defaut_group(self):
        self.assertTrue(self.regular_user.groups.filter(name='Обычные пользователи').exists(), 'Regular user does not get default group')
    def test_news_creation_permission(self):
        "Test: news creation is allowed only for create_editor and admin"
        self.client.logout()
        anonymous_user_response = self.client.get(reverse('add_news'))
        self.assertEqual(anonymous_user_response.status_code, 302, 'Anonymous user can open add_news')
        self.assertIn('/login', anonymous_user_response.url)
        admin_user_login = self.client.login(username=self.admin_user.username, password=self.admin_password)
        admin_user_response = self.client.get(reverse('add_news'))
        self.assertEqual(admin_user_response.status_code, 200, 'Admin do not have access to add_news')
        editor_user_login = self.client.login(username=self.editor_user.username, password=self.editor_password)
        editor_user_response = self.client.get(reverse('add_news'))
        self.assertEqual(editor_user_response.status_code, 200, 'Create_editor do not have access to add_news')
