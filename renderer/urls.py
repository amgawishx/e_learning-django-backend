from django.urls import path
from django.contrib import admin
from .views import index, redirect, login, assignment


urlpatterns = [
    path('home/', index, name='home'),
    path('', redirect, name="main"),
    path("login/", login , name='login'),
    path("assignment/", assignment, name='assignment')
]
