from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField


class Ticket(models.Model):
    """Model for a ticket."""
    title = models.CharField(max_length=128, help_text='Titre du billet')
    author = models.CharField(max_length=128, default='Auteur inconnu', help_text='Auteur du livre')
    description = RichTextField(max_length=2048, blank=True, help_text='Description du livre')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    """Model for a review."""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Note attribuée au livre'
    )
    headline = models.CharField(max_length=128, help_text='Titre de la critique')
    body = models.TextField(max_length=8192, blank=True, help_text='Contenu de la critique')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    """Model for a user following another user."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')
