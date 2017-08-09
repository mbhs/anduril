from django.contrib.auth.mixins import LoginRequiredMixin

from lib.views import ProfileBasedViewDispatcher

from core import models
from . import student


class GroupView(LoginRequiredMixin, ProfileBasedViewDispatcher):
    """View groups to join or manage."""

    lookup = {models.UserProfile.STUDENT: student.GroupView.as_view()}
