from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")  # add/remove fields depending on your User model

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")
