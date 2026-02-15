from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from core.models import Tutor, Profile
from core.api.serializers import TutorSerializer
from core.api.permissions import IsClinicUser


class TutorViewSet(viewsets.ModelViewSet):
    serializer_class = TutorSerializer
    permission_classes = [IsAuthenticated, IsClinicUser]

    def _get_clinic(self):
        try:
            profile = self.request.user.profile
        except Profile.DoesNotExist:
            raise PermissionDenied("Usuário sem perfil vinculado.")
        if not profile.clinic_id:
            raise PermissionDenied("Usuário sem clínica vinculada no perfil.")
        return profile.clinic

    def get_queryset(self):
        clinic = self._get_clinic()
        return Tutor.objects.filter(clinic=clinic)

    def perform_create(self, serializer):
        clinic = self._get_clinic()
        serializer.save(clinic=clinic)