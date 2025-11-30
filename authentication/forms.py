from django import forms

from authentication.models import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        required=True,
        min_length=4,
    )
    password = forms.CharField(
        label='Password',
        required=True,
        min_length=4,
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = ['username', 'password']
