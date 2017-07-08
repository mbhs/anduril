from django.conf.urls import url
from . import views

urls = [
    url("^$", views.index, name="index"),
    url("^login/$", views.login, name="login"),
    url("^logout/$", views.logout, name="logout"),
    url("^account/$", views.index, name="account")
]
