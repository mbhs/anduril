"""Model serializers for the API view."""

from rest_framework import serializers

from core import models


class UserSerializer(serializers.ModelSerializer):
    """Serializes user models."""

    profile_type = serializers.CharField(source="profile.type")

    class Meta:
        model = models.User
        fields = ("username", "email", "first_name", "last_name", "profile_type", )
