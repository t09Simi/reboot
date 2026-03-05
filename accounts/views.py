from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, CareerGapProfileForm, MentorProfileForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Reboot, {user.name}! You are not alone.")
            return redirect('core:home')
    
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form':form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.name}!")
            return redirect('core:dashboard')
        
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('core:home')

@login_required
def profile_view(request):
    # This gives logged in users profile
    profile = request.user.careergapprofile

    if request.method == "POST":
        form = CareerGapProfileForm(request.POST,request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('accounts:profile')
    else:
        form = CareerGapProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

@login_required
def mentor_profile_view(request):
    profile = request.user.mentorprofile

    if request.method == 'POST':
        form = MentorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('accounts:mentor_profile')
        
    else:
        form = MentorProfileForm(instance=profile)
    
    return render(request, 'accounts/mentor_profile.html', {'form': form, 'profile':profile})