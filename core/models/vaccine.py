from django.db import models
from .clinic import Clinic


class Vaccine(models.Model):
    # Catálogo global (não pertence a clínica)
    name = models.CharField(max_length=120, unique=True)

    # Exemplo: 365 dias para reforço
    booster_interval_days = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class ClinicVaccine(models.Model):
    # Associação N:N entre Clínica e Vaccine
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="clinic_vaccines")
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name="clinic_vaccines")

    class Meta:
        # Evita duplicar a mesma vacina associada à mesma clínica
        unique_together = ("clinic", "vaccine")

    def __str__(self):
        return f"{self.clinic.name} -> {self.vaccine.name}"
