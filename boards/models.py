from django.db import models

from authentication.models import User


class Board(models.Model):
    title = models.CharField(
        blank=False,
    )
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=False,
        related_name='owner_of_boards',
    )
    members = models.ManyToManyField(
        to=User,
        blank=False,
        related_name='member_of_boards',
    )
