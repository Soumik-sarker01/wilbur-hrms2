# task_sheet/urls.py
from django.urls import path
from . import views
from .views import task_list, update_tasks

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('login/', views.login_view, name='login'),
    path('auth_slider/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('update-tasks/', views.update_tasks, name='update_tasks'),
]
