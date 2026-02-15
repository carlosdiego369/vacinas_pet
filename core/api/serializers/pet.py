from rest_framework import serializers
from core.models import Pet


class PetSerializer(serializers.ModelSerializer):
    tutor_name = serializers.ReadOnlyField(source="tutor.name")
    species_label = serializers.CharField(source="get_species_display", read_only=True)

    class Meta:
        model = Pet
        fields = "__all__"
        read_only_fields = ["clinic"]

    def validate(self, attrs):
        request = self.context["request"]
        clinic = request.user.profile.clinic
        tutor = attrs.get("tutor")

        if tutor and tutor.clinic_id != clinic.id:
            raise serializers.ValidationError({"tutor": "Tutor não pertence à sua clínica."})

        # Em atualização, garantir que o tutor pertence à clínica do pet
        if self.instance and tutor and tutor.clinic_id != self.instance.clinic_id:
            raise serializers.ValidationError(
                {"tutor": "Tutor deve pertencer à mesma clínica do pet."}
            )

        return attrs