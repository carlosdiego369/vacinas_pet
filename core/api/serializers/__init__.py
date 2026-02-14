from .clinic import ClinicSerializer
from .tutor import TutorSerializer
from .pet import PetSerializer
from .vaccine import VaccineSerializer, ClinicVaccineSerializer
from .vaccination import VaccinationRecordSerializer

__all__ = [
    "ClinicSerializer",
    "TutorSerializer",
    "PetSerializer",
    "VaccineSerializer",
    "ClinicVaccineSerializer",
    "VaccinationRecordSerializer",
]
