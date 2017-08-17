from django.conf.urls import url
from . import views


urls = [
    url("^$", views.Index.as_view(), name="index"),
    url("^list/$", views.List.as_view(), name="list"),
    url("^create/(?P<typeof>\w+)?$", views.Create.as_view(), name="create"),
]
