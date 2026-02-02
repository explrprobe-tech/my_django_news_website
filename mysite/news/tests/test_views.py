from django.test import TestCase
from news.models import News, Category
from django.urls import reverse
from django.contrib.auth.models import User, Group


def create_editor_user(username='editor', password='EditorPass123!'):
    "Helper to create editor user"
    user = User.objects.create_user(
        username=username,
        password=password,
        email=f'{username}@example.ru'
    )
    editor_group, _ = Group.objects.get_or_create(name='Редакторы')
    user.groups.add(editor_group)
    return user, password

class NewsViewsTest(TestCase):
    "Tests for views in app News"
    def setUp(self):
        self.category_science = Category.objects.create(title="Science")
        self.news_science_published = News.objects.create(
            title = "Published Science News",
            content = "Content for the First news",
            category = self.category_science,
            is_published = True
        )
        self.news_science_unpublished = News.objects.create(
            title = "Unpublished Science News",
            content = "Content for the Second news",
            category = self.category_science,
            is_published = False
        )
        self.category_biology = Category.objects.create(title="Biology")
        self.news_biology_published = News.objects.create(
            title = "Published Biology news",
            content = "Content for biology news",
            category = self.category_biology,
            is_published = True
        )
    def test_home_news_page_status_code(self):
        """Тест: главная страница загружается"""
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
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

class RegisterViewTest(TestCase):
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/register.html')
    def test_register_view_post(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        body_reg = {
            'username': 'test_user',
            'email': 'test_user_email@mail.ru',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        response = self.client.post(reverse('register'), body_reg)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/', 'After succesfull registration should be redirect to /')
        self.assertTrue(User.objects.filter(username='test_user').exists(), 'User was not created')

class CreateNewsViewTest(TestCase):
    def setUp(self):
        self.editor_user, self.editor_password = create_editor_user()
        self.client.login(username=self.editor_user.username, password=self.editor_password)
    def test_create_news_view_get(self):
        response = self.client.get(reverse('add_news'))
        self.assertEqual(response.status_code, 200, 'Create news view are not reachable')
        self.assertTemplateUsed(response, 'news/add_news.html', 'Create news view uses wrong template')
    def test_create_news_view_post(self):
        response = self.client.post(reverse('add_news'), data={})
        self.assertEqual(response.status_code, 200, 'News was not created')