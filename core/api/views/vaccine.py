from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Vaccine, ClinicVaccine
from core.api.serializers import VaccineSerializer, ClinicVaccineSerializer
from core.api.permissions import IsTutorReadOnlyOrClinicFullAccess, IsClinicUser

class VaccineViewSet(viewsets.ModelViewSet):

    #Catálogo global.
    #Tutor: Somente Leitura
    #Clínica: Cria/Edita 

    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer
    permission_classes = [IsAuthenticated, IsTutorReadOnlyOrClinicFullAccess]

#Vínculo Clinica X Vacina
class ClinicVaccineViewSet(viewsets.ModelViewSet):
    
    #Gerenciamento feito pela clínica

    serializer_class = ClinicVaccineSerializer
    permission_classes = [IsAuthenticated, IsClinicUser]

    def get_queryset(self):
        clinic = self.request.user.profile.clinic
        return ClinicVaccine.objects.filter(clinic=clinic)
    
    def perform_create(self, serializer):
        serializer.save(clinic=self.request.user.profile.clinic)