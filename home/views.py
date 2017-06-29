from django.shortcuts import render


def login(request):
    """Login page for the home interface."""

    return render(request, "home/login.html")
