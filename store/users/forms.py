from django.contrib.auth.forms import AuthenticationForm
from django import forms
from users.models import User

class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group',
        'placeholder': "Имя пользователя"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-group',
        'placeholder': "Пароль"
    }))

    class Meta:
        model = User
        fields = ('username', 'password')