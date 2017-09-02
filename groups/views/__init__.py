from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render
from django.http import Http404

from lib.views import ProfileBasedViewDispatcher

from core.models import UserProfile
from groups.models import Group
from groups import forms

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

        allowed = permissions.allowed_groups(request.user)
        if typeof is None:
            return render(request, "groups/create/type.html", {"groups": map(Group.concrete.__getitem__, allowed)})
        if typeof not in Group.concrete:
            raise Http404

        if typeof not in allowed:
            return render(request, "groups/create/unauthorized.html", {"type": typeof})

        if request.user.has_perm("create_group"):
            return render(request, "groups/create/create.html", {"form": forms.create[typeof]})
