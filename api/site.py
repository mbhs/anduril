from django.conf.urls import url, include
from rest_framework import routers

from . import views

urls = [
    url("user/$", views.UserView.as_view()),
]
