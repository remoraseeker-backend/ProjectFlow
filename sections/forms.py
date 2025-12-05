from django import forms

from sections.models import Section


class SectionCreateForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = (
            'name',
        )


class SectionUpdateForm(SectionCreateForm):
    pass
