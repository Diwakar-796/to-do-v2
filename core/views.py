from django.shortcuts import render, redirect
from core.models import Task, Category, Feedback
from core.forms import TaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

# Create your views here.

def home(request):
    form = TaskForm()
    tasks = []
    total_task = 0
    categories = []
    recent_tasks = []
    remaining_task = 0
    total_completed_task = 0

    task_labels = []
    task_durations = []

    today = timezone.localtime().date()
    yesterday = today - timedelta(days=1)

    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user, scheduled_time__date=today).order_by('-priority')
        total_task = tasks.count()
        total_completed_task = tasks.filter(is_done=True).count()
        remaining_task = tasks.count() - total_completed_task
        recent_tasks = Task.objects.filter(user=request.user, is_done=True, updated_at__date=yesterday)
        categories = Category.objects.filter(user=request.user)

        for task in tasks:
            if task.duration:
                task_labels.append(task.title)
                task_durations.append(task.duration)
    
    context = {
        'form':form,
        'tasks':tasks,
        'total_task':total_task,
        'total_completed_task':total_completed_task,
        'remaining_task':remaining_task,
        'recent_tasks':recent_tasks,
        'categories':categories,

        'task_labels': task_labels,
        'task_durations': task_durations,
    }

    return render(request, 'core/home.html', context)

@login_required
def add_task(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            form.save()
            messages.success(request, 'Task added successfully!')
            return redirect('core:home')
        else:
            messages.error(request, 'Something went wrong!')
    
    return render(request, 'core/home.html', {'form':form})

@login_required
def done_task(request):
    if request.method == 'POST':
        user = request.user
        task_id = request.POST.get('check')
        task = Task.objects.get(user=request.user, id=task_id)

        if task.is_done:
            task.is_done = False
            if task.duration:
                user.coins_earned -= task.duration
                task.coins = 0
        else:
            task.is_done = True
            if task.duration:
                task.coins = task.duration
                user.coins_earned += task.duration

        task.updated_at = timezone.now()
        task.save()
        user.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('core:home')

@login_required
def edit_task(request, id):
    task = Task.objects.get(user=request.user, id=id)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('core:task-detail', id=id)
        else:
            messages.error(request, 'Something went wrong!')

    return render(request, 'core/task_detail.html', {'form':form})

@login_required
def del_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(user=request.user, id=id)
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('core:home')

@login_required
def search_task(request):
    if request.method == 'GET':
        form = TaskForm()
        task_labels = []
        task_durations = []

        query = request.GET.get('query')
        tasks = Task.objects.filter(Q(title__icontains=query) | Q(category__title__icontains=query) | Q(description__icontains=query))
        total_completed_task = tasks.filter(is_done=True).count()
        remaining_task = tasks.count() - total_completed_task

        for task in tasks:
            if task.duration:
                task_labels.append(task.title)
                task_durations.append(task.duration)

        context = {
            'form': form,
            'tasks': tasks,
            'remaining_task': remaining_task,
            'total_completed_task': total_completed_task,
            
            'task_labels': task_labels,
            'task_durations': task_durations,
        }

        return render(request, 'core/home.html', context)

@login_required
def task_detail(request, id):
    task = Task.objects.get(user=request.user, id=id)
    form = TaskForm(instance=task)
    context = {
        'task':task,
        'form':form,
    }
    return render(request, 'core/task_detail.html', context)

@login_required
def add_category(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        
        if title:
            Category.objects.create(
                user=request.user,
                title=title,
            )
            messages.success(request, 'Category added successfully!')
            return redirect('core:home')
        else:
            messages.error(request, 'Something went wrong!')
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')
    
@login_required
def feedback_view(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            Feedback.objects.create(
                user=request.user,
                message=message,
            )
            messages.success(request, 'Your feedback sent successfully!')
            return redirect('core:feedback')
        else:
            messages.error(request, 'Message can not be empty.')
        
    return render(request, 'core/feedback.html')
    