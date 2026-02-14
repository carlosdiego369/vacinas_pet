from rest_framework import serializers
from core.models import Tutor


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ["id", "name", "phone"]
