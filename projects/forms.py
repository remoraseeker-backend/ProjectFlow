from django import forms

from authentication.models import User
from projects.models import Project


class ProjectCreateForm(forms.ModelForm):
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
        model = Project
        fields = (
            'title',
            'members',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        members_field = self.fields['members']
        if not isinstance(members_field, forms.ModelMultipleChoiceField):
            raise TypeError()
        members_field.queryset = User.objects.all()


class ProjectUpdateForm(ProjectCreateForm):
    pass
