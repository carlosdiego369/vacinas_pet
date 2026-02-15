from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN

from core.models import Profile


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    try:
        p = request.user.profile
    except Profile.DoesNotExist:
        return Response(
            {"detail": "Perfil não configurado. Contate o administrador."},
            status=HTTP_403_FORBIDDEN,
        )
    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "role": p.role,
        "clinic_id": p.clinic_id,
        "tutor_id": p.tutor_id,
    })
