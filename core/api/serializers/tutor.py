from rest_framework import serializers
from core.models import Tutor


class TutorSerializer(serializers.ModelSerializer):
    clinic_name = serializers.CharField(source="clinic.name", read_only=True)

    class Meta:
        model = Tutor
        fields = ["id", "name", "phone", "clinic", "clinic_name"]
        read_only_fields = ["clinic"]

    def create(self, validated_data):
        # A clínica é definida na view (perform_create); DRF repassa via save(clinic=...)
        clinic = getattr(self, "clinic", None)
        if clinic is not None:
            validated_data["clinic"] = clinic
        return super().create(validated_data)
