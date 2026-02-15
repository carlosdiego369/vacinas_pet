from datetime import timedelta
from rest_framework import serializers
from core.models import VaccinationRecord, ClinicVaccine, Profile


class VaccinationRecordSerializer(serializers.ModelSerializer):
    pet_name = serializers.ReadOnlyField(source="pet.name")
    vaccine_name = serializers.ReadOnlyField(source="vaccine.name")

    class Meta:
        model = VaccinationRecord
        fields = [
            "id", "pet", "pet_name", "vaccine", "vaccine_name",
            "applied_at", "next_due_at",
        ]
        read_only_fields = ["next_due_at"]

    def validate(self, attrs):
        request = self.context.get("request")
        pet = attrs.get("pet") or (self.instance and self.instance.pet)
        vaccine = attrs.get("vaccine")
        applied_at = attrs.get("applied_at")

        if not pet or not vaccine or not applied_at:
            return attrs

        # Clínica só pode registrar/alterar vacinação de pet da própria clínica
        if request:
            try:
                profile = request.user.profile
            except Profile.DoesNotExist:
                profile = None
            if profile and profile.role == Profile.Role.CLINIC and profile.clinic_id != pet.clinic_id:
                raise serializers.ValidationError(
                    {"pet": "O pet deve pertencer à sua clínica."}
                )

        if not ClinicVaccine.objects.filter(clinic=pet.clinic, vaccine=vaccine).exists():
            raise serializers.ValidationError(
                {"vaccine": "Esta vacina não está habilitada para a clínica do pet."}
            )

        if vaccine.booster_interval_days:
            attrs["next_due_at"] = applied_at + timedelta(days=vaccine.booster_interval_days)

        return attrs
