from django.test import TestCase
from news.models import News, Category

class NewsFormTest(TestCase):
    "Tests for forms in app News"
    def setUp(self):
        self.category_science = Category.objects.create(title="Science")
        self.category_biology = Category.objects.create(title="Biology")
        self.form_data = {
            'title': 'Title for News',
            'content': 'Content for News',
            'category': self.category_science.id
        }
    def test_valid_news_form(self):
        "Test: form works with valid data"
        pass
    def test_news_form_missing_required_fields(self):
        "Test: form show errors for missing required fields"
        pass
    def test_news_form_invalid_data(self):
        "Test: form validation with invalid data"
        pass