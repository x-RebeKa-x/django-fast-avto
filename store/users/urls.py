from django.urls import path
from users.views import login, register, logout, profile, terms, privacy

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('terms-of-use/', terms, name='terms'),
    path('privacy-policy/', privacy, name='privacy')
]