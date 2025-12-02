from django.db import models

from projects.models import Project


class Section(models.Model):
    name = models.CharField(
        blank=False,
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        blank=False,
        related_name='sections',
    )

    def __str__(self) -> str:
        return self.name
