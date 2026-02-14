from datetime import timedelta
from rest_framework import serializers
from core.models import VaccinationRecord, ClinicVaccine


class VaccinationRecordSerializer(serializers.ModelSerializer):
    pet_name = serializers.ReadOnlyField(source="pet.name")
    vaccine_name = serializers.ReadOnlyField(source="vaccine.name")

    class Meta:
        model = VaccinationRecord
        fields = ["id", "pet", "pet_name", "vaccine", "vaccine_name", "applied_at", "next_due_at"]
        read_only_fields = ["next_due_at"] #Próxima dose

    def validate(self, attrs):
        pet = attrs.get("pet")
        vaccine = attrs.get("vaccine")
        applied_at = attrs.get("applied_at")

        if not pet or not vaccine or not applied_at:
            return attrs

        # Verificação da vacina se estar habilitada para a clínica do pet
        if not ClinicVaccine.objects.filter(clinic=pet.clinic, vaccine=vaccine).exists():
            raise serializers.ValidationError("Esta vacina não está habilitada para a clínica do pet.")

        # Calculo para próxima dose com o intervalo registrado pela clinica
        if vaccine.booster_interval_days:
            attrs["next_due_at"] = applied_at + timedelta(days=vaccine.booster_interval_days)

        return attrs
