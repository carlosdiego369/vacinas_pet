"""
Testes básicos da API Vacinas Pets.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from core.models import Clinic, Tutor, Pet, Vaccine, ClinicVaccine, VaccinationRecord, Profile

User = get_user_model()


class ProfileRoleTestCase(TestCase):
    """Garante que as constantes de role existem e são usadas."""

    def test_profile_roles(self):
        self.assertEqual(Profile.Role.CLINIC, "CLINIC")
        self.assertEqual(Profile.Role.TUTOR, "TUTOR")


class ClinicMultiTenantTestCase(TestCase):
    """Clínica vê apenas a própria clínica."""

    def setUp(self):
        self.client = APIClient()
        self.clinic_a = Clinic.objects.create(name="Clínica A")
        self.clinic_b = Clinic.objects.create(name="Clínica B")
        self.user_a = User.objects.create_user(username="clinic_a", password="senha123")
        Profile.objects.create(user=self.user_a, role=Profile.Role.CLINIC, clinic=self.clinic_a)

    def test_clinic_sees_only_own(self):
        self.client.force_authenticate(user=self.user_a)
        response = self.client.get("/api/clinics/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results", response.data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Clínica A")


class TutorReadOnlyTestCase(TestCase):
    """Tutor não pode criar/alterar recursos de escrita."""

    def setUp(self):
        self.client = APIClient()
        clinic = Clinic.objects.create(name="Clínica")
        tutor = Tutor.objects.create(clinic=clinic, name="Tutor", phone="")
        user = User.objects.create_user(username="tutor1", password="senha123")
        Profile.objects.create(user=user, role=Profile.Role.TUTOR, tutor=tutor, clinic=clinic)

        self.user = user
        self.clinic = clinic
        self.tutor = tutor

    def test_tutor_cannot_create_pet(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/pets/",
            {"name": "Rex", "tutor": self.tutor.id, "species": "DOG"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tutor_can_list_pets(self):
        Pet.objects.create(clinic=self.clinic, tutor=self.tutor, name="Rex", species="DOG")
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/pets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MeEndpointTestCase(TestCase):
    """GET /api/me/ retorna dados do perfil ou 403."""

    def setUp(self):
        self.client = APIClient()

    def test_me_requires_auth(self):
        response = self.client.get("/api/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_without_profile_returns_403(self):
        user = User.objects.create_user(username="noprofile", password="senha123")
        self.client.force_authenticate(user=user)
        response = self.client.get("/api/me/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_me_with_profile_returns_200(self):
        clinic = Clinic.objects.create(name="C")
        user = User.objects.create_user(username="withprofile", password="senha123")
        Profile.objects.create(user=user, role=Profile.Role.CLINIC, clinic=clinic)
        self.client.force_authenticate(user=user)
        response = self.client.get("/api/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], Profile.Role.CLINIC)
        self.assertEqual(response.data["clinic_id"], clinic.id)
