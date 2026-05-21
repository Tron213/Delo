from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import RegisterForm, loginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "Delo_app/welcome.html")

def loginPage(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Пытаемся аутентифицировать пользователя
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Если пользователь найден и пароль верен
                login(request, user)
                return redirect('/home')   # или redirect('home')
            else:
                # Если аутентификация не удалась
                form.add_error(None, 'Неверный логин или пароль')
    else:
        form = loginForm()
    
    return render(request, "Delo_app/loginPage.html", {'form': form})

def registrationPage(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Данные прошли валидацию
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Создаём пользователя
            user = User.objects.create_user(username=username, password=password)
            # (Опционально) сразу авторизуем пользователя
            # from django.contrib.auth import login
            # login(request, user)
            # Перенаправляем на другую страницу, например, 'success' или 'login'
            return redirect('/loginPage')   # Имя маршрута зададим ниже
    else:
        form = RegisterForm()
    return render(request, "Delo_app/registrationPage.html", {'form': form})


@login_required
def homePage(request):
    return render(request, "Delo_app/homePage.html")

def custom_logout(request):
    logout(request)
    return redirect('/')