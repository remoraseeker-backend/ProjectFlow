import datetime as dt

from django.db import models

from app_config.validators import datetime_not_past_validator
from authentication.models import User


class TaskPriority(models.IntegerChoices):
    URGENT = 1, 'Urgent'
    HIGH = 2, 'High'
    MEDIUM = 3, 'Medium'
    LOW = 4, 'Low'


class TaskStatus(models.TextChoices):
    TO_DO = 'TO_DO', 'To do'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    DONE = 'DONE', 'Done'


def deadline_cant_be_in_past_validator(value: dt.datetime):
    return datetime_not_past_validator(value=value, error_msg='The deadline date cant be in past.')


class Task(models.Model):
    title = models.CharField(
        blank=False,
        null=False,
        verbose_name='Title',
    )
    description = models.TextField(
        blank=False,
        null=False,
        verbose_name='Description',
    )
    priority = models.IntegerField(
        blank=False,
        null=False,
        choices=TaskPriority.choices,
        verbose_name='Priority',
    )
    status = models.CharField(
        blank=True,
        null=False,
        default=TaskStatus.TO_DO,
        choices=TaskStatus.choices,
        verbose_name='Status',
    )
    executor = models.ForeignKey(
        blank=True,
        null=True,
        to=User,
        on_delete=models.SET_NULL,
        related_name='executor_of_tasks',
        verbose_name='Executor',
    )
    creator = models.ForeignKey(
        blank=False,
        null=False,
        to=User,
        on_delete=models.CASCADE,
        related_name='creator_of_tasks',
        verbose_name='Creator',
    )
    deadline = models.DateTimeField(
        blank=True,
        null=True,
        validators=(
            deadline_cant_be_in_past_validator,
        )
        verbose_name='Deadline',
    )

    def __str__(self) -> str:
        return self.title
