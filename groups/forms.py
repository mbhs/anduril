from django.forms import ModelForm

from core import models


class GroupFrom(ModelForm):
    """Student request for group creation."""

    class Meta:
        model = models.Group
        