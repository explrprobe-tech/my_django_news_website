from django.test import TestCase
from news.models import News, Category
from news.forms import NewsForm, RegisterForm

class NewsFormTest(TestCase):
    "Tests for News forms in app News"
    def setUp(self):
        self.category_science = Category.objects.create(title="Science")
        self.category_biology = Category.objects.create(title="Biology")
        self.news_form_data = {
            'title': 'Science',
            'content': 'Content for Science News',
            'short_description': 'Short description for Science News',
            'category': self.category_science.id,
            'is_published': True
        }
    def test_news_form_valid(self):
        "Test: form works with valid data"
        form =  NewsForm(data=self.news_form_data)
        self.assertTrue(form.is_valid(), 'Form is not valid')
        news = form.save()
        self.assertIsInstance(news, News, 'News object by form is not an instance of News class')
        self.assertEqual(news.title, 'Science', 'News object by form has not title')
        self.assertEqual(news.content, 'Content for Science News', 'News object by form has not content')
        self.assertEqual(news.short_description, 'Short description for Science News', 'News object by form has not short description')
        self.assertEqual(news.category.id, self.category_science.id, 'News object by form has not category')
        self.assertTrue(news.is_published, 'News object by form does not have attribute is_published')
    def test_news_form_missing_required_fields(self):
        "Test: form shows errors only for missing required fields"
        required_fields = ['title', 'category']
        for field in required_fields:
            form_data_copy = self.news_form_data.copy()
            del form_data_copy[field]
            news_valid = NewsForm(data=form_data_copy)
            self.assertFalse(news_valid.is_valid(), f'{field} should be required')
            self.assertIn(field, news_valid.errors, f'News form does not show error for required field - {field}')
        not_required_fields = ['content', 'is_published', 'short_description']
        for field in not_required_fields:
            form_data_copy = self.news_form_data.copy()
            del form_data_copy[field]
            news_invalid = NewsForm(data=form_data_copy)
            self.assertTrue(news_invalid.is_valid(), f'{field} should not be required')
            self.assertNotIn(field, news_invalid.errors, f'News form does show error for not required field - {field}')
    def test_news_form_invalid_data(self):
        "Test: form validation with invalid data"
        news_form_data_invalid = {
            'title': '123 Invalid title',
            'short_description': 'Short description for invalid form',
            'content': 'Content for invalid form',
            'category': self.category_biology.id,
            'is_published': True
        }
        news_invalid = NewsForm(data=news_form_data_invalid)
        self.assertFalse(news_invalid.is_valid(), 'News object by invalid form should be invalid')
        self.assertIn('title', news_invalid.errors, 'Title with start by number should be invalid')
    
class RegisterFormTest(TestCase):
    "Tests for Register form in app News"
    def setUp(self):
        self.register_form_data = {
            'username': 'Test_user_form',
            'email': 'Test_user_form@mail.ru',
            'password1': 'Coplexpassword123!',
            'password2': 'Coplexpassword123!'
        }
    def test_register_form_valid(self):
        "Test: register form works with valid data"
        register = RegisterForm(data=self.register_form_data)
        self.assertTrue(register.is_valid(), f'Register form should be valid. Error: {register.errors if not register.is_valid() else None}')
        user_test = register.save()
        self.assertEqual(user_test.username, 'Test_user_form')
        self.assertEqual(user_test.email, 'Test_user_form@mail.ru')
        self.assertTrue(user_test.check_password('Coplexpassword123!'), 'user test password should match')
        self.assertTrue(user_test.is_active, 'user test should be active')
    def test_register_form_missing_required_fields(self):
        "Test: register form doesn't work with invalid data"
        required_fields = ['username', 'email', 'password1', 'password2']
        for field in required_fields:
            register_form_data_copy = self.register_form_data.copy()
            del register_form_data_copy[field]
            register_valid = RegisterForm(data=register_form_data_copy)
            self.assertFalse(register_valid.is_valid(), f'{field} should be required')
            self.assertIn(field, register_valid.errors, f'Register form does not show error for {field}')
    def test_register_form_invalid_data(self):
        "Test: Register form doesn't work with invalid data"
        register_form_data_invalid = {
            'username': 'test_user_invalid_name$',
            'email': 'invalid_mail.ru',
            'password1': 'short',
            'password2': 'does not match password1'
        }
        register_form_invalid = RegisterForm(data=register_form_data_invalid)
        self.assertFalse(register_form_invalid.is_valid())
        self.assertIn('username', register_form_invalid.errors, 'Register form does not check username $')
        self.assertIn('email', register_form_invalid.errors, 'Register form does not check email pattern')
        self.assertIn('password1', register_form_invalid.errors, 'Register form does not check password1 short')
        self.assertIn('password2', register_form_invalid.errors, 'Register form does not check password2 matching to password1')
