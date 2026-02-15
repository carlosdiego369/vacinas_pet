from rest_framework import serializers
from core.models import Vaccine, ClinicVaccine


class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ["id", "name", "booster_interval_days"]


class ClinicVaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicVaccine
        fields = ["id", "clinic", "vaccine"]
        read_only_fields = ["clinic"]

    def create(self, validated_data):
        clinic = getattr(self, "clinic", None)
        if clinic is not None:
            validated_data["clinic"] = clinic
        return super().create(validated_data)