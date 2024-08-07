from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login as auth_login
from .forms import SignUpForm, LoginForm


def home(request):
    return render(request, 'accounts/home.html', {})

def signup(request):
    """Sign up view"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    """Login view"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
             auth_login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """Logout view"""
    auth_logout(request)
    return redirect('home')
