from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Tutor
from core.api.serializers import TutorSerializer
from core.api.permissions import IsClinicUser


class TutorViewSet(viewsets.ModelViewSet):
    serializer_class = TutorSerializer
    permission_classes = [IsAuthenticated, IsClinicUser]

    def get_queryset(self):
        #Traz apenas os tutores relacionados a clinica
        clinic = self.request.user.profile.clinic
        return Tutor.objects.filter(clinic=clinic)
    
    def perform_create(self, serializer):
        clinic = self.request.user.profile.clinic
        serializer.save(clinic.self.request.user.profile.clinic)