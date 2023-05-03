from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import *
from django.views.generic.base import RedirectView

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
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
                  path('planai/', views.subscription, name='planai'),

                  path('cancel/', CancelView.as_view(), name='cancel'),
                  path('success/', SuccessView.as_view(), name='success'),
                  path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(),
                       name='create-checkout-session'),
                  path('basic/', ProductLandingPageViewBasic.as_view(), name='basic'),
                  path('premium/', ProductLandingPageViewPremium.as_view(), name='premium'),
                  path('ultra/', ProductLandingPageViewUltra.as_view(), name='ultra'),
                  path('webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),
                  path('klaidos/', views.klaidos, name='klaidos'),
                  path('cancelsub/', views.cancel_subscription, name='cancelsub'),
                  path('cancelsubsuc/', views.cancel_subscription_success, name='cancelsubsuc'),
                  

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)