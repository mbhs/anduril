from django.contrib.auth.mixins import LoginRequiredMixin

from lib.views import ProfileBasedViewDispatcher

from core import models
from . import student


class List(LoginRequiredMixin, ProfileBasedViewDispatcher):
    """View groups to join or manage."""

    lookup = {models.UserProfile.STUDENT: student.List.as_view()}


class Create(LoginRequiredMixin, ProfileBasedViewDispatcher):
    """Submit a group creation form."""

    lookup = {models.UserProfile.STUDENT: student.Create.as_view()}
