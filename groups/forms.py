from django.forms import ModelForm

from . import models


class ClubGroupRequestFrom(ModelForm):
    """Student request for group create."""

    class Meta:
        model = models.ClubGroupRequest
        fields = ["sponsors"]


requests = {models.Group.CLUB: ClubGroupRequestFrom}
create = {}
