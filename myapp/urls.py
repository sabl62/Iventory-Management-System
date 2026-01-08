# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('stock/', views.main_stock, name='main_stock'),
    path('allocate/', views.allocate_stock, name='allocate_stock'),
    path('projects/', views.projects, name='projects'),
]