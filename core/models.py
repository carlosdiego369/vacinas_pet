from django.db import models
from django.conf import settings

# Chave PK - Clínica 
class Clinic(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

# Dono do pet 
class Tutor(models.Model):
    #1:N - Clinica -> Varios Tutores
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        related_name="tutores" 
)
    
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.name} ({self.clinic.name})"
    

class Pet