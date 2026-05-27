from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import RegisterForm, loginForm, NewRoadmap, RoadmapDescription, StageTitle, RoadmapDate, TaskTitle, stepsTitle
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from django.db.models import Count

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
    
    # ОДИН запрос, который получает всё необходимое
    roadmaps = Roadmaps.objects.filter(User=request.user).annotate(
        stages_count=Count('stages', distinct=True),
        tasks_count=Count('stages__tasks', distinct=True),
        steps_count=Count('stages__tasks__steps', distinct=True)
    )
    
    context = {
        'username': username,   
        'roadmaps': roadmaps,   # Используйте только эту переменную
        'form': form,
    }
    
    return render(request, "Delo_app/homePage.html", context)

def custom_logout(request):
    logout(request)
    return redirect('/')


@login_required
def Roadmap(request, index):
    # Получаем объект Roadmaps по индексу из URL
    roadmap = get_object_or_404(Roadmaps, id=index)
    stages = Stages.objects.filter(Roadmap=index).prefetch_related(
    'tasks_set__steps_set'
)


    
    

    # Проверяем, что текущий пользователь – владелец
    if request.user != roadmap.User:
        return redirect(homePage)
    
     
    form = RoadmapDescription(instance=roadmap)
    form2 = StageTitle(instance=roadmap)
    dateForm = RoadmapDate(instance=roadmap)
    taskTitleForm = TaskTitle()
    StepForm = stepsTitle()

    if request.method == 'POST':
        # Связываем форму с существующим объектом через instance
        form = RoadmapDescription(request.POST, instance=roadmap)
        if form.is_valid():
            form.save()  
            return redirect(request.path)



    context = {
        'username': request.user.username,
        'roadmap': roadmap,
        'form': form,
        'stages':stages,
        'form2':form2,
        'dateForm':dateForm,
        'index':index,
        'taskTitleForm':taskTitleForm,
        'StepForm': StepForm,
    }
    return render(request, "Delo_app/RoadmapPage.html", context)


@login_required
def addStage(request, index):
    roadmap = get_object_or_404(Roadmaps, id=index)
    
    if roadmap.User != request.user:
        return redirect('homePage')  
    
    if request.method == 'POST':  
        form = StageTitle(request.POST)
        if form.is_valid():
            stage = form.save(commit=False)  
            stage.Roadmap = roadmap
            stage.save()  
        return redirect('Roadmap', index=index)
    
    return redirect('Roadmap', index=index)

@login_required
def Delitroadmap(request, index):
    roadmap = get_object_or_404(Roadmaps, id=index)
    
    if roadmap.User != request.user:
        return redirect('homePage')  
    instance = Roadmaps.objects.get(pk=index)
    instance.delete()
    return redirect('homePage') 

@login_required
def addRoadmapeDeadline(request, index):
    roadmap = get_object_or_404(Roadmaps, id=index)
  
    if roadmap.User != request.user:
        return redirect('homePage')  
    if request.method == 'POST':
        form = RoadmapDate(request.POST, instance=roadmap)
        print(form)

        if form.is_valid():
            form.save()
    return redirect('Roadmap', index=index)


@login_required
def addTasks(request,stage_id,index):
    roadmap = get_object_or_404(Roadmaps, id=index)
    if roadmap.User != request.user:
        return redirect('homePage') 
    stage = get_object_or_404(Stages, id=stage_id, Roadmap=roadmap)
    if request.method == 'POST':
        form = TaskTitle(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.Stage = stage  # Заполняем Stage
            task.save()
            
        return redirect('Roadmap', index=index)
    return redirect('Roadmap', index=index)

@login_required
def addSteps(request, Tasks_id, index):
    roadmap = get_object_or_404(Roadmaps, id=index)
    if roadmap.User != request.user:
        return redirect('homePage')
    
    task = get_object_or_404(
        Tasks, 
        id=Tasks_id, 
        Stage__Roadmap__id=index, 
        Stage__Roadmap__User=request.user
    )
    
    if request.method == 'POST':
        form = stepsTitle(request.POST)
        if form.is_valid():
            step = form.save(commit=False)
            step.Task = task
            step.status = 'pending'  # Добавьте значение по умолчанию
            step.save()
            
        else:
            # Логируем ошибки формы
            print(form.errors)
            
        
        return redirect('Roadmap', index=index)
    
    return redirect('Roadmap', index=index)


@login_required
def deleteStage(request, index, Stage_id):
    roadmap = get_object_or_404(Roadmaps, id=index)
    
    if roadmap.User != request.user:
        return redirect('homePage')  
    instance = Stages.objects.get(pk=Stage_id)
    instance.delete()
    return redirect('Roadmap', index=index) 