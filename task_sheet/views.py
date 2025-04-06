# task_sheet/views.py
import json
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import TaskEntry
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Signup
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # optional if you're managing roles
        if User.objects.filter(username=username).exists():
            return render(request, 'task_sheet/signup.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        # If you want to assign group/role later, we can do that too
        login(request, user)
        return redirect('task_list')  # or any other home page
    return render(request, 'accounts/auth_slider.html')



# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')  # or dashboard
        else:
            return render(request, 'task_sheet/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')



# Logout
def logout_view(request):
    logout(request)
    return redirect('login')  # redirect to login page

@login_required(login_url='login')  # Users must be logged in to access this view
def task_list(request):
    """
    Renders the task list page.
    You can pass context data if needed.
    """
    # For now, we are just rendering the template.
    return render(request, 'task_sheet/task_list.html')

@csrf_exempt
def update_tasks(request):
    """
    Receives a POST request with JSON data representing tasks.
    It then updates or creates TaskEntry records in the database.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Expecting data to be a list of task objects.
            for task in data:
                # Convert the date string into a Python date object if provided.
                task_date = (
                    datetime.strptime(task.get('date'), "%Y-%m-%d").date()
                    if task.get('date')
                    else None
                )
                TaskEntry.objects.update_or_create(
                    order_id=task.get('order_id'),
                    defaults={
                        'date': task_date,
                        'profile': task.get('profile'),
                        'client_name': task.get('client_name'),
                        'total_needed': task.get('total_needed'),
                        'previously_done': task.get('previously_done'),
                        'due_date': (
                            datetime.strptime(task.get('due_date'), "%Y-%m-%d").date()
                            if task.get('due_date')
                            else None
                        ),
                        'today_target': task.get('today_target'),
                        'project_status': task.get('project_status'),
                        'remarks': task.get('remarks'),
                        'designer1': task.get('designer1'),
                        'designer1_target': task.get('designer1_target'),
                        'designer1_done': task.get('designer1_done'),
                        'designer2': task.get('designer2'),
                        'designer2_target': task.get('designer2_target'),
                        'designer2_done': task.get('designer2_done'),
                        'designer3': task.get('designer3'),
                        'designer3_target': task.get('designer3_target'),
                        'designer3_done': task.get('designer3_done'),
                        'designer4': task.get('designer4'),
                        'designer4_target': task.get('designer4_target'),
                        'designer4_done': task.get('designer4_done'),
                        'done_today': task.get('done_today'),
                        'design_left': task.get('design_left'),
                        'total_done': task.get('total_done'),
                    }
                )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
