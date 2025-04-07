# task_sheet/views.py
import json
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import TaskEntry

@login_required(login_url='/accounts/login/')
def task_list(request):
    tasks = TaskEntry.objects.all().order_by('-date')  # Sort by most recent
    return render(request, 'task_sheet/task_list.html', {'tasks': tasks})

@csrf_exempt
def update_tasks(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for task in data:
                task_date = (datetime.strptime(task.get('date'), "%Y-%m-%d").date() 
                            if task.get('date') else None)
                TaskEntry.objects.update_or_create(
                    order_id=task.get('order_id'),
                    defaults={
                        'date': task_date,
                        'profile': task.get('profile'),
                        'client': task.get('client'),  # Changed from client_name
                        'total_design': task.get('total_design'),  # Changed from total_needed
                        'previously_done': task.get('previously_done'),
                        'due_date': (datetime.strptime(task.get('due_date'), "%Y-%m-%d").date() 
                                    if task.get('due_date') else None),
                        'today_target': task.get('today_target'),
                        'status': task.get('status'),  # Changed from project_status
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