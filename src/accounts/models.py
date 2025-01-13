# account/models.py
from django.contrib.auth.models import AbstractUser
# from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model()

class User(AbstractUser):
    pass

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     bio = models.TextField(blank=True, help_text="Une courte biographie de l'utilisateur.")
#     avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, help_text="Image de profil de l'utilisateur.")

#     def __str__(self):
#         return f"Profil de {self.user.username}"
