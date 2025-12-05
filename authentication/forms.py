from django import forms

from authentication.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )
        widgets = {
            'password': forms.PasswordInput,
        }
