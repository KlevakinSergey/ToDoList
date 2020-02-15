from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('list/', views.index, name='list'),
    path('delete/<str:pk>/', views.delete_task, name='delete'),
    path('update/<str:pk>/', views.update_task, name='update_task'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


]
