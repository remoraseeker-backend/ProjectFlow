from django.db import models

from authentication.models import User


class Project(models.Model):
    title = models.CharField(
        blank=False,
        null=False,
        verbose_name='Title',
    )
    owner = models.ForeignKey(
        blank=False,
        null=False,
        to=User,
        on_delete=models.CASCADE,
        related_name='owner_of_projects',
        verbose_name='Owner',
    )
    members = models.ManyToManyField(
        blank=True,
        to=User,
        related_name='member_of_projects',
        verbose_name='Members',
    )

    def __str__(self) -> str:
        return self.title
