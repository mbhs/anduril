from django.conf.urls import url
from . import views

urls = [
    url("^$", views.index, name="groups:index"),
]
