from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializer import ProfileSerializer

# needed to create token automatically on profile creation
from .. import models


@api_view(
    [
        "POST",
    ]
)
@permission_classes([AllowAny])
def registration(request):
    """Register new profile."""
    serializer = ProfileSerializer(data=request.data)
    resp = {}
    if serializer.is_valid():
        profile = serializer.save()

        resp["username"] = profile.username
        resp["email"] = profile.email

        token = Token.objects.get(user=profile).key
        resp["token"] = token

        resp["message"] = "Registration Successful"
    else:
        resp = serializer.errors

    return Response(resp)


@api_view(
    [
        "POST",
    ]
)
@permission_classes([AllowAny])
def logout_view(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)
