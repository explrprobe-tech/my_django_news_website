from django.test import TestCase
from news.models import News, Category
from django.urls import reverse

class NewsViewsTest(TestCase):
    "Tests for views in app News"
    def setUp(self):
        self.category_science = Category.objects.create(title="Science")
        self.news_science_published = News.objects.create(
            title = "Published News",
            content = "Content for the First news",
            category = self.category_science,
            is_published = True
        )
        self.news_science_unpublished = News.objects.create(
            title = "Unpublished News",
            content = "Content for the Second news",
            category = self.category_science,
            is_published = False
        )
        self.category_biology = Category.objects.create(title="Biology")
        self.news_biology_published = News.objects.create(
            title = "Biology news",
            content = "Content for biology news",
            category = self.category_biology,
            is_published = True
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
        news_list = response.context['news']
        news_items = list(news_list)
        self.assertEqual(len(news_items), 2, f'Должнj быть 2 новости, сейчас: {len(news_items)}')
        news_in_context = news_items[0]
        self.assertEqual(news_in_context.id, self.news_science_published.id, f'В контексте должна быть новосить с id: {self.news_science_published.id}')
        self.assertTrue(news_in_context.is_published, "Новость в контекст должна быть опубликованной")
        news_ids_in_context = [news.id for news in news_items]
        self.assertNotIn(self.news_science_unpublished.id, news_ids_in_context, f'Новосить с id: {self.news_science_unpublished.id} не должна быть в контексте')
    def test_home_news_page_template(self):
        """Тест: главная страница использует правильный шаблон"""
        response = self.client.get(reverse('news_list'))
        self.assertTemplateUsed(response, 'news/home_news_list.html')
    def test_news_detail_views_published(self):
        """Test: News can be taken"""
        response_news_published = self.client.get(self.news_science_published.get_absolute_url())
        self.assertEqual(response_news_published.status_code, 200, 'Published news status code should be 200')
        self.assertTemplateUsed(response_news_published, 'news/news_details.html')
        self.assertEqual(response_news_published.context['news_item'], self.news_science_published)
    def test_news_detail_views_unpublished(self):
        """Test: unpablished news can not be taken"""
        response_news_unpublished = self.client.get(self.news_science_unpublished)
        self.assertEqual(response_news_unpublished.status_code, 404, 'Unpublished news can be opened')
    def test_news_by_category(self):
        """Test: category returns news"""
        response_category = self.client.get(self.category_science.get_absolute_url())
        self.assertEqual(response_category.status_code, 200, "Category can not be opened")
        self.assertTemplateUsed(response_category, 'news/home_news_list.html')
    def test_news_by_category_shows_only_published(self):
        """Test: category show only published news"""
        response_category = self.client.get(self.category_science.get_absolute_url())
        category_news = response_category.context['news']
        self.assertIn(self.news_science_published, category_news, 'Published news is not in category science')
        self.assertNotIn(self.news_science_unpublished, category_news, 'Unublished news is in category science')
        self.assertNotIn(self.news_biology_published, category_news, 'Biology news is in category science')
