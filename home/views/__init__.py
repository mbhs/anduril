from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View

from core import models
from lib.utils import profile_type
from lib.views import ProfileBasedViewDispatcher

from . import student


class LoginView(View):
    """Main login view for Home."""

    def get(self, request, *args, **kwargs):
        """Get the static HTML page."""

        return render(request, "home/login.html")

    def post(self, request, *args, **kwargs):
        """Post login data to the server."""

        try:
            username = request.POST["username"]
            password = request.POST["password"]
        except KeyError:
            return HttpResponse(status=500)

        user = auth.authenticate(username=username, password=password)

        if user is None or user is False:  # Invalid username or wrong password
            response = redirect("home:login")
            response["Location"] += "?error=1"
            return response

        if not user.is_staff or not user.has_perm("can_login"):
            response = redirect("home:login")
            response["Location"] += "?error=2"
            return response

        auth.login(request, user)
        return redirect("home:index")


def logout(request):
    """Log out the currently logged in user."""

    if request.user:
        auth.logout(request)
    return redirect("home:login")


class IndexView(ProfileBasedViewDispatcher):
    """View the index page."""

    lookup = {models.UserProfile.STUDENT: student.index}
