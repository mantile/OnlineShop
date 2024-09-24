from django.urls import path
from .views import profile, register, logout_view, login_view  # Убедитесь, что добавили login_view

app_name = 'users'  # Убедитесь, что это определено
urlpatterns = [
    path('register/', register, name='register'),  # Регистрация
    path('profile/', profile, name='profile'),      # Личный кабинет
    path('logout/', logout_view, name='logout'),    # Выход
    path('login/', login_view, name='login'),       # Вход
]
