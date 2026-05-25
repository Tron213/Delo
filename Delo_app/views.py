from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import RegisterForm, loginForm, NewRoadmap, RoadmapDescription
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import get_object_or_404

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
    if request.method == 'POST':
        form = NewRoadmap(request.POST)
        
        if form.is_valid():
            RoadmapTitle = form.cleaned_data['RoadmapTitle']
            user = request.user
            record = Roadmaps.objects.create(User=user, Title=RoadmapTitle)
            new_id = record.id          
            return redirect(f'/roadmap/{new_id}/')
    else:
        form = NewRoadmap()
    username = request.user.username
    roadmaps = Roadmaps.objects.filter(User=request.user)
    context = {
            'username': username,   
            'roadmaps': roadmaps,        
        }
        

    full_context = {**context, 'form': form,}
    return render(request, "Delo_app/homePage.html", full_context)

def custom_logout(request):
    logout(request)
    return redirect('/')


@login_required
def Roadmap(request, index):
    # Получаем объект Roadmaps по индексу из URL
    roadmap = get_object_or_404(Roadmaps, id=index)

    # Проверяем, что текущий пользователь – владелец
    if request.user != roadmap.User:
        # Можно вернуть 403 или показать сообщение об ошибке
        return render(request, "Delo_app/RoadmapPage.html", {
            'error': 'У вас нет прав для редактирования этого плана.',
            'roadmap': roadmap,
            'username': request.user.username,
        })

    if request.method == 'POST':
        # Связываем форму с существующим объектом через instance
        form = RoadmapDescription(request.POST, instance=roadmap)
        if form.is_valid():
            form.save()  # обновит поле Description у roadmap
            # После успешного сохранения – редирект на эту же страницу (чтобы избежать повторной отправки формы)
            return redirect(request.path)
    else:
        # GET-запрос: показываем форму, заполненную текущим описанием
        form = RoadmapDescription(instance=roadmap)

    context = {
        'username': request.user.username,
        'roadmap': roadmap,
        'form': form,
    }
    return render(request, "Delo_app/RoadmapPage.html", context)