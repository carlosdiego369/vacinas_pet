from django.db import models
from .clinic import Clinic
from .tutor import Tutor


class Pet(models.Model):
    # Multi-tenant: pet pertence a uma clínica
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="pets")

    # Pet pertence a um tutor
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="pets")

    name = models.CharField(max_length=120)

    class Species(models.TextChoices):
        DOG = "DOG", "Cachorro"
        CAT = "CAT", "Gato"
        OTHER = "OTHER", "Outros"

    species = models.CharField(
        max_length=10,
        choices=Species.choices,
        default=Species.OTHER
    )

    def __str__(self):
        return f"{self.name} - {self.tutor.name}"
