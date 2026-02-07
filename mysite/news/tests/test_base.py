from django.contrib.auth.models import User, Group
from news.models import News

def admin_user(username='admin', password='AdminPass123!'):
    "Helper for create admin user"
    user = User.objects.create_user(
        username=username,
        password=password,
        email=f'{username}@example.ru'
    )
    admin_group, _ = Group.objects.get_or_create(name='Администраторы')
    user.groups.add(admin_group)
    return user, password

def regular_user(username='regular', password='RegularPass123!'):
    "Helper for create regular user"
    user = User.objects.create_user(
        username=username,
        password=password,
        email=f'{username}@example.ru'
    )
    return user, password

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

def with_fresh_news(func):
    "Decorator for creating fresh news"
    def wrapper(self, *args, **kwargs):
        self.created_news = News.objects.create(
            title='Title for test news',
            content='Content for test news',
            category=self.category_science
        )
        return func(self, *args, **kwargs)
    return wrapper