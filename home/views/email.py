from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View


class EmailView(LoginRequiredMixin, View):
    """Email submit and confirmation."""


