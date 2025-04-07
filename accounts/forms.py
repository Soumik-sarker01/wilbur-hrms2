# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email (e.g., john@example.com).")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# For password reset request: username and email.
class PasswordResetRequestForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

# For verifying the token: username and token.
class PasswordResetVerifyForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    token = forms.CharField(max_length=100, required=True)
