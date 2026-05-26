# forms.py
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *

class RegisterForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    # Валидация: проверяем, что пароли совпадают
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        if password and confirm and password != confirm:
            raise ValidationError('Пароли не совпадают')
        return cleaned_data

    # Валидация: проверяем уникальность логина
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует')
        return username




class loginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class NewRoadmap(forms.Form):
    RoadmapTitle = forms.CharField(
        label="Например Выучить английский язык, подготовится к свадьбе",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'input-modern',
            'placeholder': "Например Выучить английский язык, подготовится к свадьбе" 
        })
    )
class RoadmapDescription(ModelForm):
    class Meta:
        model = Roadmaps
        fields = ['Description']
        widgets = {                                 
            'Description': forms.TextInput(attrs={
                'class': 'input-modern',
                'placeholder': "Вы еще не указали описание своей цели"
            })
        }
class RoadmapDate(ModelForm):
    class Meta:
        model = Roadmaps
        fields = ['goald_date']
        {                                 
            'goald_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'input-modern'
            }),}


class StageTitle(ModelForm):
    class Meta:
        model = Stages
        fields = ['Stagetitle','goald_date']
        widgets = {                                 
            'Stagetitle': forms.TextInput(attrs={
                'class': 'input-modern',
                'placeholder': "Добавьте этап для достижения своей цели"
            }),
            'goald_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'input-modern'
            }),
        }
class TaskTitle(ModelForm):
    class Meta:
        model = Tasks
        fields = ['Tasktitle']
        widgets = {                                 
            'Stagetitle': forms.TextInput(attrs={
                'class': 'input-modern',
                'placeholder': "Добавьте задачу"
            }),
            
        }