from django.test import TestCase
from news.models import News, Category

class AuthTest(TestCase):
    "Tests for auth in app News"
    def test_user_creation(self):
        "Test creation user"
        pass