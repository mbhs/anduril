from oauth2_provider.contrib.rest_framework.permissions import TokenHasReadWriteScope, TokenHasScope
from rest_framework import permissions, viewsets

from core import models
from . import serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Views pertaining to users."""

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
