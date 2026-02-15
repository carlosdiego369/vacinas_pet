from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Pet, Profile
from core.api.serializers import PetSerializer
from core.api.permissions import IsTutorReadOnlyOrClinicFullAccess


class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated, IsTutorReadOnlyOrClinicFullAccess]

    def get_queryset(self):
        p = self.request.user.profile
        if p.role == Profile.Role.CLINIC:
            return Pet.objects.filter(clinic=p.clinic)

        return Pet.objects.filter(tutor=p.tutor)
    
    def perform_create(self, serializer):
        #Cadastro de tutor somente a clinica haverá permissão
        serializer.save(clinic=self.request.user.profile.clinic)
