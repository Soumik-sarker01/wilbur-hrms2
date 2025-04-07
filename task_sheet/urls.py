from django.urls import path
from .views import task_list, update_tasks

urlpatterns = [
    path('', task_list, name='task_list'),
    path('update-tasks/', update_tasks, name='update_tasks'),
]
