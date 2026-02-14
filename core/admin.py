from django.contrib import admin
from core.models import Clinic, Tutor, Pet, Vaccine, ClinicVaccine, VaccinationRecord, Profile

admin.site.register(Clinic)
admin.site.register(Tutor)
admin.site.register(Pet)
admin.site.register(Vaccine)
admin.site.register(ClinicVaccine)
admin.site.register(VaccinationRecord)
admin.site.register(Profile)
