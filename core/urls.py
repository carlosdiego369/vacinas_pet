from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.api.views import (
    ClinicViewSet,
    TutorViewSet,
    PetViewSet,
    VaccineViewSet,
    ClinicVaccineViewSet,
    VaccinationRecordViewSet,
    me,
)

router = DefaultRouter()
router.register(r"clinics", ClinicViewSet, basename="clinic")
router.register(r"tutors", TutorViewSet, basename="tutor")
router.register(r"pets", PetViewSet, basename="pet")
router.register(r"vaccines", VaccineViewSet, basename="vaccine")
router.register(r"clinic-vaccines", ClinicVaccineViewSet, basename="clinic-vaccine")
router.register(r"vaccinations", VaccinationRecordViewSet, basename="vaccination")

urlpatterns = [
    path("me/", me),
    path("", include(router.urls)),
]
