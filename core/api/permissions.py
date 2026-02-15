from rest_framework.permissions import BasePermission, SAFE_METHODS
from core.models import Profile

def _has_profile(user) -> bool:
    return user.is_authenticated and hasattr(user, "profile")


class IsClinicUser(BasePermission):
    def has_permission(self, request, view):
        if not _has_profile(request.user):
            return False
        try:
            return request.user.profile.role == Profile.Role.CLINIC
        except Profile.DoesNotExist:
            return False


class IsTutorReadOnlyOrClinicFullAccess(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        try:
            profile = user.profile
        except Profile.DoesNotExist:
            return False

        if profile.role == Profile.Role.CLINIC:
            return True

        if profile.role == Profile.Role.TUTOR:
            return request.method in SAFE_METHODS

        return False

