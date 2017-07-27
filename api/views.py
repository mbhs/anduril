from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.contrib.rest_framework.permissions import TokenHasReadWriteScope, TokenHasScope
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from core import models
from . import serializers


class UserView(views.APIView):
    """Get user information."""

    queryset = models.User.objects

    authentication_classes = (OAuth2Authentication,)
    permission_classes = (TokenHasScope,)
    required_scopes = ("read",)

    def get(self, request, format=None):
        """Get the user view."""

        print(request.user)
        return Response({})
