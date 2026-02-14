from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import VaccinationRecord
from core.api.serializers import VaccinationRecordSerializer
from core.api.permissions import IsTutorReadOnlyOrClinicFullAccess


class VaccinationRecordViewSet(viewsets.ModelViewSet):
    serializer_class = VaccinationRecordSerializer
    permission_classes = [IsAuthenticated, IsTutorReadOnlyOrClinicFullAccess]

    def get_queryset(self):
        profile = self.request.user.profile

        # Isolamento: clínica vê registros dos pets dela; tutor só dos próprios pets
        if profile.role == "CLINIC":
            return VaccinationRecord.objects.filter(pet__clinic=profile.clinic)

        return VaccinationRecord.objects.filter(pet__tutor=profile.tutor)
