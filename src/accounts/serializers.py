from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()

# Serializer du profil utilisateur
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']  # Champs du profil

# Serializer des utilisateurs avec profil imbriqué
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True, default=None)  # Imbrication du profil, lecture seule

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']  # Champs retournés pour l'utilisateur
