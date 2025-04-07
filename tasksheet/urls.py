from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Redirect root "/" to the login page
def redirect_to_login(request):
    return redirect('/accounts/login/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('task_sheet.urls')),    # Task-related URLs
    path('accounts/', include('accounts.urls')),     # Authentication URLs
    path('', redirect_to_login),                     # Redirect root to login
]
