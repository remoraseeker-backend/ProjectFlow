from django import forms

from authentication.models import User
from boards.models import Board


class BoardCreateForm(forms.ModelForm):
    title = forms.CharField(
        label='Title',
        required=True,
    )
    members = forms.ModelMultipleChoiceField(
        label='Members',
        required=False,
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Board
        fields = ['title', 'members']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        members_field = self.fields['members']
        if not isinstance(members_field, forms.ModelMultipleChoiceField):
            raise TypeError()
        members_field.queryset = User.objects.all()
