from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from django.http import Http404

from lib.views import ProfileBasedViewDispatcher

from core.models import UserProfile
from groups.models import Group
from . import student

from lib import permissions


class Index(LoginRequiredMixin, ProfileBasedViewDispatcher):
    """View the group index page."""

    lookup = {UserProfile.STUDENT: student.index}


class List(LoginRequiredMixin, ProfileBasedViewDispatcher):
    """View groups to join or manage."""

    lookup = {UserProfile.STUDENT: student.List.as_view()}


class Create(LoginRequiredMixin, View):
    """Create a new group."""

    def get(self, request, *args, typeof=None, **kwargs):
        """Get the form."""

        if typeof is None:
            allowed = permissions.allowed_groups(request.user)
            return render(request, "groups/type.html", {"groups": allowed})
        if typeof not in Group.concrete:
            raise Http404

        if typeof == Group.CLUB:
            pass
