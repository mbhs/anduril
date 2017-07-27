"""Model serializers for the API view."""

from rest_framework import serializers

from core import models


class UserSerializer(serializers.ModelSerializer):
    """Serializes user models."""

    class Meta:
        model = models.User
