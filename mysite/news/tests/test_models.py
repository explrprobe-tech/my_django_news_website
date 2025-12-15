from django.test import TestCase
from news.models import News, Category
from django.contrib.auth.models import User
from django.urls import reverse

class NewsModelTest(TestCase):
    """Тесты для модели News"""
    
    def test_news_creation(self):
        # 1. Create Category and News for this category
        category = Category.objects.create(title="Technology")
        news = News.objects.create(
            title="First test news",
            content="Test content for first news",
            category=category
        )
        
        # 2. Check that category and news were created correct
        self.assertEqual(news.title, "First test news")
        self.assertEqual(category.title, "Technology")
        self.assertEqual(news.category.title, "Technology")
    
    def test_news_str_method(self):
        """Тест: правильно ли отображается новость?""" #TODO BY MYSELF
        # Здесь будет второй тест
        pass

class NewsViewsTest(TestCase):
    """Тесты для представлений"""

    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        password='testpass123')
        self.category = Category.objects.create(title="Science")

        self.news_published = News.objects.create(
            title = "Published News",
            content = "Content for the First news",
            category = self.category,
            is_published = True
        )
        self.news_unpublished = News.objects.create(
            title = "UnPublished News",
            content = "Content for the Second news",
            category = self.category,
            is_published = False
        )

    def test_home_news_page_status_code(self):
        """Тест: главная страница загружается"""

        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)

    def test_home_news_page_shows_news_published(self): 
        """Тест: публикованная новость отображается"""

        response = self.client.get(reverse('news_list'))

        self.assertEqual(response.status_code, 200)

        self.assertIn('news', response.context, 'В контексте должен быть ключ news_list')

        #получаем query_set из контекста
        news_list = response.context['news']

        #преобразуем в список для удобства проверки
        news_items = list(news_list)

        self.assertEqual(len(news_items), 1, f'Должна быть 1 новость, сейчас: {len(news_items)}')

        #вытаскием первую новость из списка
        news_in_context = news_items[0]

        self.assertEqual(news_in_context.id, self.news_published.id, f'В контексте должна быть новосить с id: {self.news_published.id}')

        self.assertTrue(news_in_context.is_published, "Новость в контекст должна быть опубликованной")

        #преобразуем в список id для удобства проверок
        news_ids_in_context = [news.id for news in news_items]
        self.assertNotIn(self.news_unpublished.id, news_ids_in_context, f'Новосить с id: {self.news_unpublished.id} не должна быть в контексте')

    def test_home_news_page_template(self):
        """Тест: главная страница использует правильный шаблон"""

        response = self.client.get(reverse('news_list'))

        self.assertTemplateUsed(response, 'news/home_news_list.html')