from rest_framework.permissions import BasePermission, SAFE_METHODS


def _has_profile(user) -> bool:
    return user.is_authenticated and hasattr(user, "profile")


class IsClinicUser(BasePermission):
    def has_permission(self, request, view):
        return _has_profile(request.user) and request.user.profile.role == "CLINIC"


class IsTutorReadOnlyOrClinicFullAccess(BasePermission):
    """
    Clínica: CRUD completo
    Tutor: apenas leitura
    """
    def has_permission(self, request, view):
        if not _has_profile(request.user):
            return False

        role = request.user.profile.role
        if role == "CLINIC":
            return True
        if role == "TUTOR":
            return request.method in SAFE_METHODS
        return False
