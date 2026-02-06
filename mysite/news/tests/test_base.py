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

def create_news(category, **kwargs):
    "Helper for create news"
    default_data = {
        'title': 'Title for Test News',
        'content': 'Content for Test News',
        'category': category,
        'is_published': True
    }
    default_data.update(kwargs)
    return News.objects.create(**default_data)