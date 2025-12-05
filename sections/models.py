from django.db import models

from projects.models import Project


class Section(models.Model):
    name = models.CharField(
        blank=False,
        null=False,
        verbose_name='Name',
    )
    project = models.ForeignKey(
        blank=False,
        null=False,
        to=Project,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name='Project',
    )

    def __str__(self) -> str:
        return self.name
