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
        self.assertTrue(form.is_valid())
        news = form.save()
        self.assertIsInstance(news, News, 'News object by form is not an instance of News class')
        self.assertEqual(news.title, 'Science', 'News object by form has not title')
        self.assertEqual(news.content, 'Content for Science News', 'News object by form has not content')
        self.assertEqual(news.category, self.category_science.id, 'News object by form has not category')
        self.assertTrue(news.is_published, 'News object by form does not have attribute is_published')
    def test_news_form_missing_required_fields(self):
        "Test: form show errors for missing required fields"
        pass
    def test_news_form_invalid_data(self):
        "Test: form validation with invalid data"
        pass