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
 #Leitura do ID quando o user está logado e indetifica a clinica para qual ele está cadastrado