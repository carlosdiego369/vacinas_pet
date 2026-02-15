from django.db import models
from .pet import Pet
from .vaccine import Vaccine


class VaccinationRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="vaccinations")
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name="vaccinations")

    #Quando foi aplicado
    applied_at = models.DateField()
    #Próxima dose
    next_due_at = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("pet", "vaccine", "applied_at")
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.pet.name} - {self.vaccine.name} ({self.applied_at})"
