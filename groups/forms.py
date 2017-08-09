from django.forms import ModelForm

from core import models


class GroupFrom(ModelForm):
    """Student request for group creation."""

    class Meta:
        model = models.Group

    # TODO: implement two part form, first page group type, then individual forms
