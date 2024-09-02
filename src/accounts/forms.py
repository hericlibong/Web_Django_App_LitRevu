from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    """Form for user registration."""
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"})
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'})
    )
    password2 = forms.CharField(
        label="Confirmez",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmez mot de passe'})
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2')

    def clean_password1(self):
        """Check if the two passwords match."""
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError('Le mot de passe doit contenir au moins 8 caractères')
        if not any(char.isdigit() for char in password1):
            raise ValidationError('Le mot de passe doit contenir au moins un chiffre')
        if not any(char.isupper() for char in password1):
            raise ValidationError('Le mot de passe doit contenir au moins une lettre majuscule')
       
        return password1

    def clean_password2(self):
        """Check if the two passwords match."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('les mots de passe ne correspondent pas')

        return password2


class LoginForm(forms.Form):
    """Form for user login."""
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'})
    )
