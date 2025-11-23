from django.test import TestCase
from news.models import News, Category

class NewsModelTest(TestCase):
    """Тесты для модели News"""
    
    def test_news_creation(self):
        # 1. Create Category and News for this category
        category = Category.objects.create(name="Technology")
        news = News.objects.create(
            title="First test news",
            content="Test content for first news",
            category=category
        )
        
        # 2. Check that category and news were created correct
        self.assertEqual(news.title, "First test news")
        self.assertEqual(news.category, "Technology")
    
    def test_news_str_method(self):
        """Тест: правильно ли отображается новость?"""
        # Здесь будет второй тест
        pass