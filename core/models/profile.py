from django.conf import settings
from django.db import models

from .clinic import Clinic
from .tutor import Tutor


class Profile(models.Model):
    class Role(models.TextChoices):
        CLINIC = "CLINIC", "Clinic"
        TUTOR = "TUTOR", "Tutor"

    # User padrão do Django (username/password)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(max_length=10, choices=Role.choices)

    # Se for CLINIC user, aponta para a clínica
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True)

    # Se for TUTOR user, aponta para o tutor
    tutor = models.OneToOneField(Tutor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
