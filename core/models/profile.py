from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

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

    def clean(self):
        # 1) Se role = CLINIC, não pode ter tutor
        if self.role == "CLINIC" and self.tutor_id:
            raise ValidationError({"tutor": "Usuário CLINIC não deve ter tutor vinculado."})

        # 2) Se role = TUTOR, precisa ter tutor
        if self.role == "TUTOR" and not self.tutor_id:
            raise ValidationError({"tutor": "Usuário TUTOR precisa ter tutor vinculado."})

        # 3) Se tem tutor e clinic, eles precisam ser da mesma clínica
        if self.tutor_id and self.clinic_id and self.tutor.clinic_id != self.clinic_id:
            raise ValidationError({"tutor": "Tutor deve pertencer à mesma clínica do Profile."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
