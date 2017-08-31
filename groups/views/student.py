from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, FormView

from groups import models


@login_required
def index(request):
    """View the index groups page."""

    return render(request, "groups/student/index.html", {"groups": request.user.groups.all()})


class List(ListView):
    """View the list of available groups."""

    model = models.Group
    template_name = "groups/student/list.html"
    context_object_name = "groups"
    paginate_by = 25
