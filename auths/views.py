from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from auths.forms import SignUpForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Task
from django.utils import timezone
from datetime import datetime, timedelta

# Create your views here.

def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('auths:sign_in')
        else:
           messages.error(request, 'Something went wrong!') 

    return render(request, 'auths/sign_up.html', {'form':form})

def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}')
            return redirect('core:home')
        else:
            messages.error(request, 'User does not exist.')

    return render(request, 'auths/sign_in.html')

@login_required
def sign_out(request):
    logout(request)
    messages.success(request, 'Logout successfully!')
    return redirect('auths:sign_in')

@login_required
def profile_view(request):
    total_tasks = Task.objects.filter(user=request.user).count()
    completed_tasks = Task.objects.filter(is_done=True).count()
    pending_tasks = total_tasks - completed_tasks

    context = {
        'total_tasks':total_tasks,
        'completed_tasks':completed_tasks,
        'pending_tasks':pending_tasks,
    }

    return render(request, 'auths/profile.html', context)

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

    return render(request, 'auths/profile.html', context)

@login_required
def edit_profile_view(request):
    form = EditProfileForm(instance=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('auths:profile')
        else:
            messages.error(request, 'Something went wrong!')
    
    return render(request, 'auths/edit_profile.html', {'form':form})