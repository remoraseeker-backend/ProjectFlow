from django import forms

from sections.models import Section


class SectionCreateForm(forms.ModelForm):
    name = forms.CharField(
        label='Name',
        required=True,
    )

    class Meta:
        model = Section
        fields = ['name']


class SectionUpdateForm(SectionCreateForm):
    pass
