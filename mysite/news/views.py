from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import requests


from .models import News, Category
from .forms import NewsForm, RegisterForm, CategoryForm

# Проверка что пользователь в группе "Администраторы"
def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Администраторы').exists()

# Проверка что пользователь в группе "Редакторы" или "Администраторы"
def is_editor_or_admin(user):
    return user.is_superuser or user.groups.filter(name__in=['Редакторы', 'Администраторы']).exists()

def home(request):
    latest_news = News.objects.all().order_by('-created_at').filter(is_published=True)[:3]
    can_add_news = is_editor_or_admin(request.user)
    can_see_secret_page = is_editor_or_admin(request.user)
    return render(request, 'news/home.html', {
        'latest_news': latest_news,
        'can_add_news': can_add_news,
        'can_see_secret_page': can_see_secret_page
    })

def admin_required(view_func):
    "Custom decorator that returns 403 for non-admins"
    def wrapper(request, *args, **kwargs):
        if not is_editor_or_admin(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

def get_data(url) -> dict:
    """Universal function to fetch JSON data"""
    try:
        r = requests.get(url, timeout=5)
        return r.json()[0]
    except:
        return {} 

@login_required
@admin_required
def secret_page(request):
    # Get solar radio flux data from NOAA API (first element only)
    sun_data = get_data('https://services.swpc.noaa.gov/json/solar-radio-flux.json')
    
    # Get timestamp from the data
    timestamp = sun_data.get('time_tag', 'Unknown')
    station = sun_data.get('common_name', 'Unknown')
    
    # Extract frequency details for display
    frequencies = sun_data.get('details', [])[0]
    
    return render(request, 'news/secret_page.html', {
        'station': station,
        'timestamp': timestamp,
        'frequencies': frequencies,
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Автоматически добавляем в группу "Обычные пользователи"
            try:
                default_group = Group.objects.get(name='Обычные пользователи')
                user.groups.add(default_group)
            except Group.DoesNotExist:
                pass  # Группы нет, оставляем без группы
            
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')

            if request.headers.get('User-Agent') == 'MyAutotestBot/1.0':
                return JsonResponse({
                    'status': 'success',
                    'user_id': f'user/{user.id}/'
                })
            
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'news/register.html', {'form': form})

@login_required
@require_http_methods(["POST"])
def category_delete(request, pk):
    """Delete category by API"""
    if not is_editor_or_admin(request.user):
        messages.error(request, 'У вас нет прав на удаление категории')
        return redirect('categories_list')
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, f'Категория {category.title} успешно удалена')
    return redirect('categories_list')

@login_required
@require_http_methods(["POST"])
def user_delete(request, user_id):
    """Delete user by API"""
    try:
        user = User.objects.get(id=user_id)
        if not is_admin(request.user):
            return JsonResponse({'error': 'You do not have permission to delete users'}, status=403)
        username = user.username
        user.delete()
        return JsonResponse({'error': f'User {username} deleted successefully!'}, status=200)
    except:
        return JsonResponse({'error': 'User not found'}, status=400)

@login_required
@require_http_methods(["POST"])
def news_delete(request, pk):
    """Delete news by API"""
    if not is_editor_or_admin(request.user):
        messages.error(request, "У вас нет прав на удаление новости")
        return redirect('news_list')
    news = get_object_or_404(News, pk=pk)
    news.delete()
    messages.success(request, f'Новость {news.title} успешно удалена')
    return redirect('news_list')

@require_http_methods(["GET", "POST"])
def custom_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('home')

class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'latest_news'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home Page'
        return context
    
    def get_queryset(self):
        return News.objects.filter(is_published=True)
    
class ViewCategories(ListView):
    model = Category
    template_name = 'news/categories_list.html'
    context_object_name = 'categories_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_add_category"] = is_editor_or_admin(self.request.user)
        return context

class CreateCategory(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'news/add_category.html'
    login_url = 'accounts/login'

    def test_func(self):
        return is_editor_or_admin(self.request.user)

    def form_valid(self, form):
        """Called when form is valid"""
        messages.success(self.request, f'Категория "{form.instance.title}" успешно добавлена!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Called when form is invalid"""
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)
    
    
class NewsByCategory(ListView):
    model = News
    template_name = 'news/category_news_list.html'
    context_object_name = 'latest_news'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context
    
    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)
    
class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    template_name = 'news/news_details.html'

    def get_object(self, queryset=None):
        news = super().get_object(queryset)
        news.increment_views()
        return news
    
class CreateNews(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = 'accounts/login'

    def test_func(self):
        return is_editor_or_admin(self.request.user)
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class EditNews(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/edit_news.html'
    context_object_name = 'news_item'
    
    def test_func(self):
        return is_editor_or_admin(self.request.user)
    
    def get_success_url(self):
        return reverse('view_news', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        if self.request.POST.get('photo-clear'):
            if self.object.photo:
                self.object.photo.delete()
                self.object.photo = None
                self.object.save()
        return super().form_valid(form)
