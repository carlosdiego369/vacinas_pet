from django.db import models
from .clinic import Clinic
from .tutor import Tutor
from django.core.exceptions import ValidationError



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

    def clean(self):
        # tutor tem que ser da mesma clínica do pet
        if self.tutor_id and self.clinic_id and self.tutor.clinic_id != self.clinic_id:
            raise ValidationError({"tutor": "Tutor deve pertencer à mesma clínica do Pet."})

    def save(self, *args, **kwargs):
        self.full_clean()  # chama clean() antes de salvar
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.tutor.name}"
