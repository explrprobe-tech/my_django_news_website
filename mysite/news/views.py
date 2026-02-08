from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group


from .models import News, Category
from .forms import NewsForm, RegisterForm

# Проверка что пользователь в группе "Администраторы"
def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Администраторы').exists()

# Проверка что пользователь в группе "Редакторы" или "Администраторы"
def is_editor_or_admin(user):
    return user.groups.filter(name__in=['Редакторы', 'Администраторы']).exists()

def home(request):
    return render(request, 'news/home.html')

def admin_required(view_func):
    "Custom decorator that returns 403 for non-admins"
    def wrapper(request, *args, **kwargs):
        if not is_editor_or_admin(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@admin_required
def secret_page(request):
    return render(request, 'news/secret_page.html')

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
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'news/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def custom_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('home')

class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home Page'
        return context
    
    def get_queryset(self):
        return News.objects.filter(is_published=True)
    
class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False 
    
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
    
class CreateNews(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = 'accounts/login'

    def test_func(self):
        return is_editor_or_admin(self.request.user)
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class EditNews(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/edit_news.html'
    context_object_name = 'news_item'
    
    def test_func(self):
        return is_editor_or_admin(self.request.user)
    
    def get_success_url(self):
        return reverse('view_news', kwargs={'pk': self.object.pk})
