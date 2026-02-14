from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    p = getattr(request.user, "profile", None)
    return Response({
        "id": request.user.id,
        "username": request.user.username,
        "role": getattr(p, "role", None),
        "clinic_id": getattr(p, "clinic_id", None),
        "tutor_id": getattr(p, "tutor_id", None),
    })
