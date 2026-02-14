from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Clinic
from core.api.serializers import ClinicSerializer
from core.api.permissions import IsClinicUser


class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    permission_classes = [IsAuthenticated, IsClinicUser]
