from django.conf.urls import url
from . import views


urls = [
    url("^list/$", views.List.as_view(), name="index"),
    url("^create/$", views.Create.as_view(), name="index"),
]
