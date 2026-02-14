from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Tutor
from core.api.serializers import TutorSerializer
from core.api.permissions import IsClinicUser
from rest_framework.exceptions import ValidationError


class TutorViewSet(viewsets.ModelViewSet):
    serializer_class = TutorSerializer
    permission_classes = [IsAuthenticated, IsClinicUser]

    def _get_clinic(self):
        profile = getattr(self.request.user, "profile", None)
        if not profile or not profile.clinic:
            raise ValidationError({"detail": "Usuário sem clínica vinculada no Profile."})
        return profile.clinic

    def get_queryset(self):
        clinic = self._get_clinic()
        return Tutor.objects.filter(clinic=clinic)

    def perform_create(self, serializer):
        clinic = self._get_clinic()
        serializer.save(clinic=clinic)