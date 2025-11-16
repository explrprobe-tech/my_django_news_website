from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class BasicTests(TestCase):
    def test_home_page(self):
        """Тест главной страницы"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Новости')
    
    def test_admin_login(self):
        """Тест страницы входа в админку"""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # Редирект на логин
    
    def test_user_creation(self):
        """Тест создания пользователя"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')