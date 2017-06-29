from django.conf.urls import url
from . import views

urls = [
    url("^login/", views.login, name="login")
]
