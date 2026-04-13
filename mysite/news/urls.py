from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.NewsByCategory.as_view(), name='category_id'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('category/add_category/', views.CreateCategory.as_view(), name='add_category'),
    path('category/', views.ViewCategories.as_view(), name='categories_list'),

    path('news/<int:pk>/', views.ViewNews.as_view(), name='view_news'),
    path('news/<int:pk>/delete/', views.news_delete, name='news_delete'),
    path('news/add_news/', views.CreateNews.as_view(), name='add_news'),
    path('news/', views.HomeNews.as_view(), name='news_list'),

    path('secret/', views.secret_page, name='secret_page'),

    path('register/', views.register, name='register'),
    path('user/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='news/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),

    path('news/<int:pk>/edit/', views.EditNews.as_view(), name='edit_news'),
]
