from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
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


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-group',
        'placeholder': "Введите имя"
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group',
        'placeholder': "Введите Фамилию"
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-group',
        'placeholder': "Введите никнейм"
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-group',
        'placeholder': "Введите пароль"
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-group',
        'placeholder': "Подтвердите пароль"
    }))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")

class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True, 'class': 'profile-nickname'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'profile-fullname'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'profile-fullname'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')