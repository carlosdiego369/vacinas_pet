from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from core.models import Clinic
from core.api.serializers import ClinicSerializer
from core.api.permissions import IsClinicUser


class ClinicViewSet(viewsets.ModelViewSet):
    """Cada usuário clínica vê e edita apenas a própria clínica. Criar clínica não permitido pela API."""
    serializer_class = ClinicSerializer
    permission_classes = [IsAuthenticated, IsClinicUser]

    def get_queryset(self):
        profile = self.request.user.profile
        if profile.clinic_id is None:
            return Clinic.objects.none()
        return Clinic.objects.filter(pk=profile.clinic_id)

    def perform_create(self, serializer):
        raise PermissionDenied("Criação de clínica não permitida pela API. Use o admin.")
