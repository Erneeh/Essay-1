from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import re_path as url


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.index, name='index'),
                  path('paskyra/', views.paskyra, name='paskyra'),
                  path('services/', views.services, name='services'),
                  path('login/', views.loginas, name='login'),
                  path('register/', views.register, name='register'),
                  path('logout/', views.logoutuser, name='logout'),
                  path('contacts/', views.contacts, name='contacts'),
                  path('paklausk/', views.paklausk, name='paklausk'),
                  path('rasiniai/', views.rasiniai, name='rasiniai'),
                  path('motyvacinis/', views.motyvacinis, name='motyvacinis'),
                  path('perfrazuok/', views.perfrazuok, name='perfrazuok'),
                  path('cv/', views.cv, name='cv'),
                  path('testas/', views.testas, name='testas'),
                  path('anglu/', views.anglu, name='anglu'),
                  path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
                  path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
                       name='password_reset_confirm'),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
                  path('planai/', views.subscription, name='planai'),
                  path('subscribe/', views.subscribe, name='subscribe'),
                  path('subscribed/', views.subscribed, name='subscribed'),
                  path('sub/', views.end_sub, name='sub'),
                  path('payment/', views.call_back_url, name='payment'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)