from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from core.models import VaccinationRecord, Profile
from core.api.permissions import IsTutorReadOnlyOrClinicFullAccess
from core.api.serializers import VaccinationRecordSerializer


class VaccinationRecordViewSet(viewsets.ModelViewSet):
    serializer_class = VaccinationRecordSerializer
    permission_classes = [IsAuthenticated, IsTutorReadOnlyOrClinicFullAccess]

    def get_queryset(self):
        profile = self.request.user.profile

        if profile.role == Profile.Role.CLINIC:
            return VaccinationRecord.objects.filter(pet__clinic=profile.clinic)

        if profile.role == Profile.Role.TUTOR:
            return VaccinationRecord.objects.filter(pet__tutor=profile.tutor)

        return VaccinationRecord.objects.none()

    def perform_create(self, serializer):
        profile = self.request.user.profile
        if profile.role != Profile.Role.CLINIC:
            raise PermissionDenied("Somente clínica pode registrar vacinação.")
        serializer.save()