import datetime as dt
from typing import Any

from django import forms
from django.contrib import admin

from app_config.widgets import ClientTimezoneOffsetWidget
from tasks.models import Task


class TaskAdminForm(forms.ModelForm):
    client_timezone_offset = forms.FloatField(
        required=False,
        widget=ClientTimezoneOffsetWidget()
    )

    def clean(self) -> dict[str, Any]:
        deadline = self.cleaned_data['deadline']
        if not isinstance(deadline, dt.datetime):
            return super().clean()

        client_offset = self.cleaned_data['client_timezone_offset']
        if not isinstance(client_offset, float):
            raise TypeError('Client offset must have a float type.')

        client_timezone = dt.timezone(offset=dt.timedelta(hours=client_offset))
        new_deadline = deadline.replace(tzinfo=client_timezone)
        self.cleaned_data['deadline'] = new_deadline
        return super().clean()

    class Meta:
        model = Task
        fields = '__all__'


class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm


admin.site.register((
    Task,
), TaskAdmin)
