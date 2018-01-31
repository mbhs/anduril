from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View


class EmailView(LoginRequiredMixin, View):
    """Email submit and confirmation."""

    def get(self, request):
        """Get the email view."""

        return render(request, "home/email.html")
