from django.test import TestCase
from news.models import News, Category
from django.urls import reverse

class NewsViewsTest(TestCase):
    "Tests for views in app News"
    def setUp(self):
        self.category = Category.objects.create(title="Science")
        self.news_published = News.objects.create(
            title = "Published News",
            content = "Content for the First news",
            category = self.category,
            is_published = True
        )
        self.news_unpublished = News.objects.create(
            title = "Unpublished News",
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
    def test_news_detail_views_published(self): #todo
        """Test: News can be taken"""
        response_news_published = self.client.get(self.news_published.get_absolute_url())
        self.assertEqual(response_news_published.status_code, 200, 'Published news status code should be 200')
