from django.db import models
from .clinic import Clinic


class Vaccine(models.Model):
    name = models.CharField(max_length=120, unique=True)
    booster_interval_days = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ClinicVaccine(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="clinic_vaccines")
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name="clinic_vaccines")

    class Meta:
        unique_together = ("clinic", "vaccine")
        ordering = ["clinic", "vaccine"]

    def __str__(self):
        return f"{self.clinic.name} -> {self.vaccine.name}"
