from django.shortcuts import render, redirect, HttpResponse

from core import models


def index(request, *args, **kwargs):
    """The index view for students."""

    if request.user.profile.type == models.UserProfile.STUDENT:
        return render(request, "home/student/index.html")
