from django.test import TestCase
from news.models import News, Category
from django.urls import reverse
from news.tests.test_base import create_editor_user

class NewsModelTest(TestCase):
    """Тесты для модели News"""
    def setUp(self):
        self.user, _ = create_editor_user()
        self.category = Category.objects.create(title="Science")
        self.news_published = News.objects.create(
            title = "Published News",
            content = "Content for the First news",
            category = self.category,
            is_published = True,
            author = self.user,
            views_count = 0
        )
    def test_news_initial_views_count(self):
        self.assertEqual(self.news_published.views_count, 0)
    def test_increment_views_method(self):
        self.news_published.increment_views()
        self.news_published.refresh_from_db()
        self.assertEqual(self.news_published.views_count, 1)
    def test_news_creation(self):
        """Test: news were created properly"""
        self.assertIsNotNone(self.news_published.title)
        self.assertIsNotNone(self.news_published.content)
    def test_news_str_method(self):
        """Test: news displays properly"""

        self.assertEqual(str(self.news_published), self.news_published.title)
    def test_news_belongs_to_category(self):
        """Test: news belongs to category"""
        self.assertIn(self.news_published, self.category.news_set.all(), 'Published News doesnt belong to category')
    def test_news_get_absolute_url(self):  
        """Test: news can return absolute url"""
        published_url = self.news_published.get_absolute_url()
        self.assertTrue(published_url.startswith('/'), 'Published news url should start with /')
        expected_url = reverse('view_news', kwargs={'pk': self.news_published.pk})
        self.assertEqual(published_url, expected_url, 'Published news url does not match expected url')    
    def test_category_get_absolute_url(self):
        """Test: category can return absolute url"""
        category_url = self.category.get_absolute_url()
        self.assertTrue(category_url.startswith('/'), 'Category url should start with /')
        expected_url = reverse(viewname="category", kwargs={'category_id': self.category.pk})
        self.assertEqual(category_url, expected_url, 'Category url do not equal to expected')
    def test_category_str_method(self):
        """Test: category displays properly"""
        self.assertEqual(str(self.category), self.category.title) 
