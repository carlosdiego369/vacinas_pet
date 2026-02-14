from django.contrib import admin
from core.models import Clinic, Tutor, Pet, Vaccine, ClinicVaccine, VaccinationRecord, Profile

admin.site.register(Clinic)
admin.site.register(Tutor)
admin.site.register(Vaccine)
admin.site.register(ClinicVaccine)
admin.site.register(VaccinationRecord)



@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "clinic", "tutor", "species")
    list_filter = ("clinic", "species")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # quando for escolher Tutor, filtra pela clínica selecionada (se der pra inferir)
        if db_field.name == "tutor":
            # tenta pegar clinic_id vindo do form (?clinic=) ou do objeto editado
            clinic_id = request.GET.get("clinic") or request.GET.get("clinic_id")
            if clinic_id:
                kwargs["queryset"] = kwargs["queryset"].filter(clinic_id=clinic_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.clinic_id:
            form.base_fields["tutor"].queryset = Tutor.objects.filter(clinic_id=obj.clinic_id)
        return form
