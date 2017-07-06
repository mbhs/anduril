from django.shortcuts import render
from core import models


def index(request):
    """Return the example index page."""

    return render(request, "home/index.html")


def login(request):
    """Login page for the home interface."""

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password)

    return render(request, "home/login.html")

