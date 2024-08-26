# feed/forms.py

from django import forms
from django.contrib.auth import get_user_model
from .models import Review, Ticket
from ckeditor.widgets import CKEditorWidget

User = get_user_model()

class TicketForm(forms.ModelForm):
    """Form for adding a tucket"""
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Ticket
        fields = ['title', 'author', 'description', 'image']    


class UserFollowForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur', max_length=150,
                               widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Cet utilisateur n'existe pas.")
        return username


class ReviewForm(forms.ModelForm):
    """Form for adding a review to a ticket."""
    rating = forms.ChoiceField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        widget=forms.RadioSelect,
        label="Rating"
    )
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']