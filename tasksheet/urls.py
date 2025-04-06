from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Redirect root "/" to "/tasks/"
def redirect_to_tasks(request):
    return redirect('/tasks/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('task_sheet.urls')),
    path('', redirect_to_tasks),  # This redirects "/" to "/tasks/"
]
