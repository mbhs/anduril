from django.shortcuts import render
from django.views.generic import ListView

from core import models


class GroupView(ListView):
    """View the list of available groups."""

    model = models.Group
    template_name = "groups/student/index.html"
    context_object_name = "groups"
    paginate_by = 25
