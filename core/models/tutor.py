from django.db import models
from .clinic import Clinic


class Tutor(models.Model):
    # 1:N -> Uma clínica pode ter vários tutores
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="tutors")

    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.name} ({self.clinic.name})"
