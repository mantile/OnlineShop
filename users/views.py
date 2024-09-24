from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .forms import ProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Profile  # Убедитесь, что вы импортировали Profile


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # замените на вашу форму, если используете кастомную
        if form.is_valid():
            form.save()  # Сохраняем пользователя
            # Перенаправляем на страницу продуктов после успешной регистрации
            return redirect('products:product_list')  # или использовать reverse('products')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

@login_required  # Защищаем доступ к личному кабинету
def profile(request):
    # Получаем профиль текущего пользователя, если он существует
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)  # Заполняем экземпляр формы текущими данными профиля
        if form.is_valid():
            form.save()
            return redirect('users:profile')  # Перенаправляем обратно на страницу профиля после сохранения
    else:
        form = ProfileForm(instance=profile)  # Заполняем форму текущими данными профиля

    return render(request, 'users/profile.html', {'form': form})

def logout_view(request):
    logout(request)  # Выход из системы
    return redirect('users:login')  # Перенаправление на страницу входа (измените на нужный вам URL)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Вход пользователя
            next_url = request.GET.get('next', 'users:profile')  # Получение следующего URL или перенаправление на профиль по умолчанию
            return redirect(next_url)  # Перенаправление
        else:
            return render(request, 'users/login.html', {'error': 'Неверное имя пользователя или пароль.'})
    else:
        return render(request, 'users/login.html')