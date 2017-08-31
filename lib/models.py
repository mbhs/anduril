from django.db import models


class TimeTrackingModel(models.Model):
    """Tracks creation and modification date times."""

    creation_time = models.DateTimeField(auto_now_add=True)
    modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
