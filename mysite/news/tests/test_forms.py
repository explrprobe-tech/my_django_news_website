from django.test import TestCase
from news.models import News, Category
from news.forms import NewsForm

class NewsFormTest(TestCase):
    "Tests for forms in app News"
    def setUp(self):
        self.category_science = Category.objects.create(title="Science")
        self.category_biology = Category.objects.create(title="Biology")
        self.form_data = {
            'title': 'Science',
            'content': 'Content for Science News',
            'category': self.category_science.id,
            'is_published': True
        }
    def test_valid_news_form(self):
        "Test: form works with valid data"
        form =  NewsForm(data=self.form_data)
        self.assertTrue(form.is_valid(), 'Form is not valid')
        news = form.save()
        self.assertIsInstance(news, News, 'News object by form is not an instance of News class')
        self.assertEqual(news.title, 'Science', 'News object by form has not title')
        self.assertEqual(news.content, 'Content for Science News', 'News object by form has not content')
        self.assertEqual(news.category, self.category_science.id, 'News object by form has not category')
        self.assertTrue(news.is_published, 'News object by form does not have attribute is_published')
    def test_news_form_missing_required_fields(self):
        "Test: form shows errors only for missing required fields"
        required_fields = ['title', 'category']
        for field in required_fields:
            form_data_copy = self.form_data.copy()
            del form_data_copy[field]
            form = NewsForm(data=form_data_copy)
            self.assertFalse(form.is_valid(), f'{field} should be required')
            self.assertIn(field, form.errors, f'Form does not show error for required field - {field}')
        not_required_fields = ['content', 'is_published']
        for field in not_required_fields:
            form_data_copy = self.form_data.copy()
            del form_data_copy[field]
            form = NewsForm(data=form_data_copy)
            self.assertTrue(form.is_valid(), f'{field} should not be required')
            self.assertNotIn(field, form.errors, f'Form does show error for not required field - {field}')
    def test_news_form_invalid_data(self):
        "Test: form validation with invalid data"
        form_data_invalid = {
            'title': '123 Invalid title',
            'content': 'Content for invalid form',
            'category': self.category_biology.id,
            'is_published': True
        }
        news_invalid = NewsForm(data=form_data_invalid)
        self.assertFalse(news_invalid.is_valid(), 'News object by invalid form should be invalid')
        self.assertIn('title', news_invalid.errors, 'Title with start by number should be invalid')