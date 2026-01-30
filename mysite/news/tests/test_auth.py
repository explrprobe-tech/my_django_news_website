from django.test import TestCase
from news.models import News, Category
from news.views import register

class AuthTest(TestCase):
    "Tests for auth in app News"
    def setUp(self):
        pass
    def test_secret_page_requires_only_admin(self):
        pass
    def test_user_gets_defaut_group(self):
        pass
    def test_news_creation_permission(self):
        pass