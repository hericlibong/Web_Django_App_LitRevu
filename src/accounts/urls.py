from django.urls import path, include
from .views import signup, logout_view, login_view, ProfileDetailView, ProfileUpdateView, ProfileCreateView, ProfileApiViewSet, UserViewSet
from rest_framework.routers import DefaultRouter



app_name = 'accounts'

router = DefaultRouter()
router.register(r'profiles', ProfileApiViewSet, basename='profile')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),  # Page de consultation du profil
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),  # Page de modification du profil
    path('profile/create/', ProfileCreateView.as_view(), name='profile_create'),
    path('api/', include(router.urls)),
]
