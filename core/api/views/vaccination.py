from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from core.models import VaccinationRecord
from core.api.permissions import IsTutorReadOnlyOrClinicFullAccess
from core.api.serializers import VaccinationRecordSerializer



class VaccinationRecordViewSet(viewsets.ModelViewSet):
    serializer_class = VaccinationRecordSerializer
    permission_classes = [IsAuthenticated, IsTutorReadOnlyOrClinicFullAccess]

    def get_queryset(self):
        profile = self.request.user.profile

        # Clínica vê tudo da própria clínica
        if profile.role == "CLINIC":
            return VaccinationRecord.objects.filter(pet__clinic=profile.clinic)

        # Tutor vê só as vacinações dos pets dele
        if profile.role == "TUTOR":
            return VaccinationRecord.objects.filter(pet__tutor=profile.tutor)

        return VaccinationRecord.objects.none()

    def perform_create(self, serializer):
        # Tutor não chega aqui (permite só leitura), mas por segurança:
        profile = self.request.user.profile
        if profile.role != "CLINIC":
            raise PermissionDenied("Somente clínica pode registrar vacinação.")
        serializer.save()