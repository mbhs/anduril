from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import Permission

from core import models


def index(request, *args, **kwargs):
    """The index view for students."""

    return render(request, "home/student/index.html")


def profile(request, *args, **kwargs):
    """View the student profile."""

    return render(request, "home/student/profile.html")
