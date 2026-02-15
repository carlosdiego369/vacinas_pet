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
        # CLINIC
        if self.role == self.Role.CLINIC:
            if not self.clinic_id:
                raise ValidationError({"clinic": "Usuário CLINIC precisa ter uma clínica vinculada."})
            if self.tutor_id:
                raise ValidationError({"tutor": "Usuário CLINIC não deve ter tutor vinculado."})

        # TUTOR
        if self.role == self.Role.TUTOR:
            if not self.tutor_id:
                raise ValidationError({"tutor": "Usuário TUTOR precisa ter tutor vinculado."})
        # força clinic = tutor.clinic
            if self.clinic_id and self.clinic_id != self.tutor.clinic_id:
                raise ValidationError({"clinic": "Clinic do Profile deve ser a mesma clinic do Tutor."})
            if not self.clinic_id:
                self.clinic = self.tutor.clinic


    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
