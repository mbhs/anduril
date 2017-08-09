from django.shortcuts import render
from django.views.generic import ListView, FormView

from core import models


class List(ListView):
    """View the list of available groups."""

    model = models.Group
    template_name = "groups/student/list.html"
    context_object_name = "groups"
    paginate_by = 25


class Create(FormView):
    """Create a new group."""


