from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import permission_required, login_required
from core import models


def login(request):
    """Login page for the home interface."""

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff or user.has_perm("can_login"):
                auth.login(request, user)
                return redirect("index")
            response = redirect("login")
            response["Location"] += "?error=2"
            return response
        response = redirect("login")
        response["Location"] += "?error=1"
        return response
    return render(request, "home/login.html")


@login_required()
def logout(request):
    """Log out the currently logged in user."""

    if request.user:
        auth.logout(request)
    return redirect("login")


@login_required
def index(request):
    """Return the example index page."""

    return render(request, "home/index.html")
