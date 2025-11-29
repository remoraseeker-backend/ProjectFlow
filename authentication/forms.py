from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='Username',
        min_length=1,
    )
    password = forms.CharField(
        label='Password',
        min_length=1,
        widget=forms.PasswordInput(),
    )
