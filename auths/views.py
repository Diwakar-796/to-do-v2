from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from auths.forms import SignUpForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    return render(request, 'auths/profile.html')

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