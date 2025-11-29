from django import forms


class BoardCreateForm(forms.Form):
    title = forms.CharField(
        label='Title',
        min_length=1,
    )
