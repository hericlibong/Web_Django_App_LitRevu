from django.urls import path
from .views import signup, logout_view, login_view, ProfileDetailView, ProfileUpdateView, ProfileCreateView

app_name = 'accounts'

urlpatterns = [
    path('', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),  # Page de consultation du profil
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),  # Page de modification du profil
    path('profile/create/', ProfileCreateView.as_view(), name='profile_create'),
]
