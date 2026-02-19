from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.html import format_html  


from .models import News, Category

# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at', 'update_at', 'category', 'is_published', 'photo_preview') #Вывести поля в админке
    list_display_links = ('id', 'title') #Открыть объект по ссылке на этих полях
    search_fields = ('title', 'content') #Поиск объектов по этим полям
    list_editable = ('is_published',) #Разрешить редактировать поля в таблице
    list_filter = ('is_published','category') #Разрешить фильтр для полей
    fields = ('title', 'content', 'category', 'photo', 'is_published') 
    readonly_fields = ('created_at', 'update_at', 'photo_preview')

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px; border-radius: 5px; border: 2px solid #ffaa00;" />',
                obj.photo.url
            )
        return "No photo"
    photo_preview.allow_tags = True
    photo_preview.short_description = 'Photo Preview'
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

    def has_permission(self, request):
        return request.user.is_active and request.user.groups.filter(name='Администраторы').exists()


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)