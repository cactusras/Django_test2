
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from myApp import views


urlpatterns = [
    path("", views.home, name="home"),
    path("index/", views.index, name="index"),
    path('login/', views.login_view, name='login')
]