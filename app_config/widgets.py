from django import forms
from django.conf import settings


def get_static_url() -> str:
    static_url = url if (url := settings.STATIC_URL) is not None else 'static/'
    return static_url


class ClientTimezoneOffsetWidget(forms.HiddenInput):
    class Media:
        js = (
            f'{get_static_url()}js/clientTimezoneOffsetPicker.js',
        )

    def __init__(self, attrs=None):
        default_attr = {'class': 'clientTimezoneOffsetPicker'}
        if attrs:
            default_attr.update(attrs)
        super().__init__(default_attr)
