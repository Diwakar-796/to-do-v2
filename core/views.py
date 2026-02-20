from django.shortcuts import render, redirect
from core.models import Task, Category, Feedback, Notification
from core.forms import TaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Q

# Create your views here.

def check_notifications(user):
    now = timezone.now()

    tasks = Task.objects.filter(
        user=user,
        is_done=False,
        is_notified=False,
        scheduled_time__lte=now
    )

    for task in tasks:
        Notification.objects.create(
            user=user,
            task=task,
            message=f"You scheduled {task.title} for {task.duration} minutes."
        )

        task.is_notified = True
        task.save()

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

        check_notifications(request.user)

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
            task.save()
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
        notification = Notification.objects.filter(user=request.user, task=task).first()

        if task.is_done:
            task.is_done = False
            task.is_notified = False
            if notification:
                notification.is_read = False
                notification.save()
            if task.duration:
                user.coins_earned -= task.duration
                task.coins = 0
        else:
            task.is_done = True
            if notification:
                notification.is_read = True
                notification.save()
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
        tasks = Task.objects.filter(user=request.user).filter(Q(title__icontains=query) | Q(category__title__icontains=query) | Q(description__icontains=query))
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

def about_view(request):
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

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'core/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, id):
    notification = Notification.objects.get(user=request.user, id=id)
    notification.is_read = True
    notification.save()
    return redirect('core:notifications')

@login_required
def analytics(request):
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(user=request.user, is_done=True).count()
    pending_tasks = total_tasks - completed_tasks

    if request.method == 'GET':
        today = timezone.localtime().date()

        start_date = request.GET.get('start')
        end_date = request.GET.get('end')

        if start_date and end_date:
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
        else:
            start = today - timedelta(days=7)
            end = today
        
        tasks = Task.objects.filter(user=request.user, is_done=True, updated_at__date__range=[start, end])

        task_labels = []
        task_durations = []
        time_spent = 0

        for task in tasks:
            if task.duration:
                task_labels.append(task.title)
                task_durations.append(task.duration)
                time_spent = time_spent + task.duration

        context = {
            'tasks': tasks,
            'time_spent': time_spent,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,

            'task_labels': task_labels,
            'task_durations': task_durations,
        }

    return render(request, 'core/analytics.html', context)