from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('restart/', views.restart_game, name='restart'),  # Restart game URL
]
