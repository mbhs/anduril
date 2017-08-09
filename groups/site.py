from django.conf.urls import url
from . import views


urls = [
    url("^$", views.GroupView.as_view(), name="index"),
]
