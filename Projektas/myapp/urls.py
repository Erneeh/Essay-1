from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
