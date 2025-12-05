from django.db import models

from authentication.models import User


class Project(models.Model):
    title = models.CharField(
        blank=False,
        null=False,
    )
    owner = models.ForeignKey(
        blank=False,
        null=False,
        to=User,
        on_delete=models.CASCADE,
        related_name='owner_of_projects',
    )
    members = models.ManyToManyField(
        blank=True,
        to=User,
        related_name='member_of_projects',
    )

    def __str__(self) -> str:
        return self.title
