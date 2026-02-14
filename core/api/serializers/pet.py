from rest_framework import serializers
from core.models import Pet


class PetSerializer(serializers.ModelSerializer):
    tutor_name = serializers.ReadOnlyField(source="tutor.name")
    species_label = serializers.CharField(source="get_species_display", read_only=True)

    class Meta:
        model = Pet
        fields = ["id", "name", "species", "species_label", "tutor", "tutor_name"]
