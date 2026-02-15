from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from core.models import Vaccine, ClinicVaccine, Profile
from core.api.serializers import VaccineSerializer, ClinicVaccineSerializer
from core.api.permissions import IsTutorReadOnlyOrClinicFullAccess, IsClinicUser


class VaccineViewSet(viewsets.ModelViewSet):
    """Catálogo global de vacinas. Tutor: leitura. Clínica: CRUD."""
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer
    permission_classes = [IsAuthenticated, IsTutorReadOnlyOrClinicFullAccess]


class ClinicVaccineViewSet(viewsets.ModelViewSet):
    """Vínculo clínica x vacina. Apenas perfil clínica."""
    serializer_class = ClinicVaccineSerializer
    permission_classes = [IsAuthenticated, IsClinicUser]

    def _get_clinic(self):
        try:
            profile = self.request.user.profile
        except Profile.DoesNotExist:
            return None
        return profile.clinic

    def get_queryset(self):
        clinic = self._get_clinic()
        if clinic is None:
            return ClinicVaccine.objects.none()
        return ClinicVaccine.objects.filter(clinic=clinic)

    def perform_create(self, serializer):
        clinic = self._get_clinic()
        if clinic is None:
            raise PermissionDenied("Usuário sem clínica vinculada.")
        serializer.save(clinic=clinic)