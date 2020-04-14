"""sbr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from game import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', views.HealthCheckView.as_view()),
    path('create/', views.CreateGameView.as_view()),
    path('join/', views.JoinGameView.as_view()),
    path('start/', views.StartGameView.as_view()),
    path('vote/create/', views.CreateVoteView.as_view()),
    path('vote/', views.VoteView.as_view()),
    path('state/', views.GameStateView.as_view()),
]
