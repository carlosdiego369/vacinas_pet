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
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="tutors")
    
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.name} ({self.clinic.name})"
    

class Pet(models.Model):
    #Relacionamento do PET com a Clinica
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="pets")
    #Relacionamento do PET com o tutor
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="pets")
    
    name = models.CharField(max_length=120)
    
    #Criado a class interna para não fugir do padrão os registros
    class Species(models.TextChoices):
        DOG = "Cachorro", "CACHORRO"
        CAT = "Gato", "GATO"
        OTHER = "Outros", "OUTROS"

    species = models.CharField(
        max_length=10,
        choices=Species.choices,
        default=Species.OTHER
    )

    def __str__(self):
        return f"{self.name} - {self.tutor.name}"
    

class Vaccine(models.Model):
    #Catalogo global, as vacinas seram associadas a clinica evitando varias telas de cadastro
    name = models.CharField(max_length=120, unique=True)
    #Tempo para alerta de outra dose/reforço
    booster_interval_days = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class ClinicVaccine(models.Model):
    #Vinculo das vacinas que a clinica fornece para os pets
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="clinic_vaccines")
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name="clinic_vaccines")

    class Meta:
        #unificando as FK composta por clinic+vaccine
        unique_together = ("clinic", "vaccine")

    def __str__(self):
        return f"{self.clinic.name} -> {self.vaccine.name}"