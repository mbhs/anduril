from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from django.http import Http404

from lib.views import ProfileBasedViewDispatcher

from core import models
from . import student


class Index(LoginRequiredMixin, ProfileBasedViewDispatcher):
    """View the group index page."""

    lookup = {models.UserProfile.STUDENT: student.index}


class List(LoginRequiredMixin, ProfileBasedViewDispatcher):
    """View groups to join or manage."""

    lookup = {models.UserProfile.STUDENT: student.List.as_view()}


class Create(LoginRequiredMixin, View):
    """Create a new group."""

    def get(self, request, *args, typeof=None, **kwargs):
        """Get the form."""

        if typeof is None:
            return render(request, "groups/student/type.html")
        if typeof not in models.Group.concrete:
            raise Http404
