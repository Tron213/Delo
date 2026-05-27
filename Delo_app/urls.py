from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("welcome/", views.index, name="welcome"),
    path("registrationPage/", views.registrationPage, name="registrationPage"),
    path("loginPage/", views.loginPage, name="loginPage"),
    path("home/", views.homePage, name="homePage"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path("home/", views.homePage, name="homePage"),
    path('roadmap/<int:index>/', views.Roadmap, name='Roadmap'),
    path('roadmap/<int:index>/addStage', views.addStage, name='addStage'),
    path('roadmap/<int:index>/DelitRoadmap', views.Delitroadmap, name='Delitroadmap'),
    path('roadmap/<int:index>/addRoadmapeDeadline', views.addRoadmapeDeadline, name='addRoadmapeDeadline'),
    path('roadmap/<int:index>/stage/<int:stage_id>/add-task/', views.addTasks, name='addTasks'),
    path('roadmap/<int:index>/Task/<int:Tasks_id>/add-step/', views.addSteps, name='addSteps'),
    path('roadmap/<int:index>/stage/<int:Stage_id>/deleteStage/', views.deleteStage, name='deleteStage'),

]