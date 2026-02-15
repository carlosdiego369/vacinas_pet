from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Clinic
from core.api.serializers import ClinicSerializer
from core.api.permissions import IsClinicUser


class ClinicViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicSerializer
    permission_classes = [IsAuthenticated, IsClinicUser]

    def get_queryset(self):
        """Clínica vê apenas a própria clínica (multi-tenant)."""
        profile = self.request.user.profile
        if profile.clinic_id is None:
            return Clinic.objects.none()
        return Clinic.objects.filter(pk=profile.clinic_id)
