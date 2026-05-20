import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from .models import Task
from .forms import TaskForm

def task_dashboard(request):
    """
    Renders the main dashboard layout.
    """
    # Fetch initial stats
    tasks = Task.objects.all()
    stats = {
        'total': tasks.count(),
        'todo': tasks.filter(status='todo').count(),
        'in_progress': tasks.filter(status='in_progress').count(),
        'completed': tasks.filter(status='completed').count(),
        'high_priority': tasks.filter(priority='high').count(),
    }
    return render(request, 'tasks/dashboard.html', {'stats': stats})

def task_list_partial(request):
    """
    Renders the task board or list view filtered by search query and priority.
    Called via HTMX to update the view dynamically.
    """
    q = request.GET.get('q', '').strip()
    priority = request.GET.get('priority', '').strip()
    view_type = request.GET.get('view_type', 'kanban').strip()
    
    tasks = Task.objects.all()
    
    if q:
        tasks = tasks.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if priority:
        tasks = tasks.filter(priority=priority)
        
    context = {
        'view_type': view_type,
        'q': q,
        'priority': priority,
    }
    
    if view_type == 'kanban':
        context.update({
            'todo_tasks': tasks.filter(status='todo'),
            'in_progress_tasks': tasks.filter(status='in_progress'),
            'completed_tasks': tasks.filter(status='completed'),
        })
    else:
        context.update({
            'tasks': tasks
        })
        
    return render(request, 'tasks/partials/task_list_container.html', context)

def task_stats_partial(request):
    """
    Renders only the statistics cards, triggered when task counts change.
    """
    tasks = Task.objects.all()
    stats = {
        'total': tasks.count(),
        'todo': tasks.filter(status='todo').count(),
        'in_progress': tasks.filter(status='in_progress').count(),
        'completed': tasks.filter(status='completed').count(),
        'high_priority': tasks.filter(priority='high').count(),
    }
    return render(request, 'tasks/partials/stats.html', {'stats': stats})

def task_create(request):
    """
    Handles task creation.
    GET: Returns the form HTML to load in a modal.
    POST: Creates task and triggers board & stats refresh with a toast notification.
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            response = HttpResponse(status=204) # No content, tells HTMX to do nothing to current node
            response['HX-Trigger'] = json.dumps({
                'task-list-changed': True,
                'stats-changed': True,
                'show-toast': f"Task '{task.title}' created successfully!"
            })
            return response
    else:
        # Initial status can be passed as query parameter
        initial_status = request.GET.get('status', 'todo')
        form = TaskForm(initial={
            'status': initial_status,
            'priority': 'medium'
        })
        
    return render(request, 'tasks/partials/task_form.html', {
        'form': form,
        'action_url': request.path,
        'title': 'Create New Task'
    })

def task_edit(request, pk):
    """
    Handles task editing.
    GET: Returns pre-filled form HTML to load in a modal.
    POST: Updates task and triggers board & stats refresh with a toast notification.
    """
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            response = HttpResponse(status=204)
            response['HX-Trigger'] = json.dumps({
                'task-list-changed': True,
                'stats-changed': True,
                'show-toast': f"Task '{task.title}' updated successfully!"
            })
            return response
    else:
        form = TaskForm(instance=task)
        
    return render(request, 'tasks/partials/task_form.html', {
        'form': form,
        'action_url': request.path,
        'title': f"Edit Task: {task.title}"
    })

def task_update_status(request, pk):
    """
    Quick status update endpoint (e.g., clicking column arrows or moving task).
    Expects POST request with 'status'.
    """
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            response = HttpResponse(status=204)
            response['HX-Trigger'] = json.dumps({
                'task-list-changed': True,
                'stats-changed': True,
                'show-toast': f"Task status updated to '{task.get_status_display()}'."
            })
            return response
    return HttpResponse(status=400)

def task_delete(request, pk):
    """
    Handles task deletion.
    POST: Deletes task and triggers board/stats updates with a success toast.
    """
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        title = task.title
        task.delete()
        response = HttpResponse(status=204)
        response['HX-Trigger'] = json.dumps({
            'task-list-changed': True,
            'stats-changed': True,
            'show-toast': f"Task '{title}' deleted."
        })
        return response
    
    # Optional safety prompt
    return render(request, 'tasks/partials/task_delete_confirm.html', {
        'task': task
    })

def task_detail(request, pk):
    """
    Renders detail view in modal.
    """
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/partials/task_detail.html', {'task': task})
