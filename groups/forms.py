from django.forms import ModelForm

from . import models


class ClubGroupRequestFrom(ModelForm):
    """Student request for group creation."""

    class Meta:
        model = models.ClubGroup
        #fields = []
