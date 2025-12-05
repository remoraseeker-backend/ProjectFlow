import datetime as dt

from django.core.exceptions import ValidationError


def datetime_not_past_validator(value: dt.datetime, error_msg: str):
    if value >= dt.datetime.now(value.tzinfo):
        return
    current_time = dt.datetime.now(value.tzinfo).isoformat(sep=' ', timespec='seconds')
    message = f'{error_msg} Current time of your browser: {current_time}'
    raise ValidationError(message=message, code='invalid_datetime_field_value')
