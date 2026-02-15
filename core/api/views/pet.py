from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from core.models import Pet, Profile
from core.api.serializers import PetSerializer
from core.api.permissions import IsTutorReadOnlyOrClinicFullAccess


class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated, IsTutorReadOnlyOrClinicFullAccess]

    def get_queryset(self):
        p = self.request.user.profile
        if p.role == Profile.Role.CLINIC:
            if p.clinic_id is None:
                return Pet.objects.none()
            return Pet.objects.filter(clinic=p.clinic)
        return Pet.objects.filter(tutor=p.tutor)

    def perform_create(self, serializer):
        profile = self.request.user.profile
        if profile.clinic_id is None:
            raise PermissionDenied("Usuário clínica sem clínica vinculada.")
        serializer.save(clinic=profile.clinic)
