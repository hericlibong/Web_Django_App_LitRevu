from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def login_view(request):
    """View function for handling user login."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('feed:feed')  # Redirection mise à jour
            else:
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """View function for handling user logout."""
    auth_logout(request)
    return redirect('accounts:login')


def signup(request):
    """View function for handling user signup."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('feed:feed')  # Redirection mise à jour

    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
