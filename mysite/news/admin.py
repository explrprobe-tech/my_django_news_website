from django.contrib import admin
from django.contrib.auth.models import Group, User


from .models import News, Category

# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at', 'update_at', 'category', 'is_published') #Вывести поля в админке
    list_display_links = ('id', 'title') #Открыть объект по ссылке на этих полях
    search_fields = ('title', 'content') #Поиск объектов по этим полям
    list_editable = ('is_published',) #Разрешить редактировать поля в таблице
    list_filter = ('is_published','category') #Разрешить фильтр для полей
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

    def has_permission(self, request):
        return request.user.is_active and request.user.groups.filter(name='Администраторы').exists()


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)