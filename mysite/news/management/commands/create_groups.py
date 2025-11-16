from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import News

class Command(BaseCommand):
    help = 'Создает стандартные группы пользователей'
    
    def handle(self, *args, **options):
        # Группа "Обычные пользователи"
        regular_users, created = Group.objects.get_or_create(name='Обычные пользователи')
        
        # Группа "Редакторы"
        editors, created = Group.objects.get_or_create(name='Редакторы')
        news_content_type = ContentType.objects.get_for_model(News)
        news_permissions = Permission.objects.filter(content_type=news_content_type)
        editors.permissions.set(news_permissions)
        
        # Группа "Администраторы" 
        admins, created = Group.objects.get_or_create(name='Администраторы')
        # Администраторы получают все права через is_staff
        
        self.stdout.write(self.style.SUCCESS('Группы успешно созданы!'))