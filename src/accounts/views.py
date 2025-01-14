# accounts/views.py
from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Profile
from django.contrib.auth import get_user_model
from .forms import SignUpForm, LoginForm, ProfileForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import ProfileSerializer, UserSerializer

User = get_user_model()

class AdminOnlyViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


# Vue pour afficher tous les utilisateurs avec leur profil
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()  # Récupère tous les utilisateurs
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Permission pour accéder à la liste des utilisateurs

# Vue API pour lister les profils utilisateurs
class ProfileApiViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  # Permission pour accéder à la liste des profils


# Vue pour créer un nouveau profil utilisateur
class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('accounts:profile_detail')

    def form_valid(self, form):
        # Associer le profil à l'utilisateur connecté
        form.instance.user = self.request.user
        return super().form_valid(form)
    

# Vue pour afficher le profil de l'utilisateur
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        # Si l'utilisateur n'a pas de profil, rediriger vers la création de profil
        if not hasattr(self.request.user, 'profile'):
            return redirect('accounts:profile_create')
        return self.request.user.profile

# Vue pour mettre à jour le profil de l'utilisateur
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile_detail')

    def get_object(self):
        # Récupérer le profil de l'utilisateur connecté
        return self.request.user.profile



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
