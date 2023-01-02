from django.urls import path
from . import views

urlpatterns = [
    path('login-usuario/', views.login_usuario, name='login-usuario'),
    path('painel-app/', views.painel_app, name='painel-app'),
]