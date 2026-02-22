from django import forms
from .models import News
import re

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        #fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category', 'photo', 'short_description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'short_description': forms.Textarea(attrs={'class': 'form-comtrol', 'rows': 5})
        }
        
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Name must not start with a number')
        return title
    
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = 'Только буквы, цифры и @/./+/-/_'
        self.fields['password1'].help_text = 'Пароль должен быть не менее 8 символов'

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        try:
            validate_password(password=password1)
        except ValidationError as e:
            self.add_error('password1', e)
        
        return password1