from core.models import Vaccine, ClinicVaccine
from rest_framework import serializers


class VaccineSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ["id", "name", "booster_interval_day"]


class ClinicVaccineSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClinicVaccine
        fields = ["id", "clinic", "vaccine"]
        read_only_fields = ["clinic"] #Leitura do ID quando o user está logado e indetifica a clinica para qual ele está cadastrado