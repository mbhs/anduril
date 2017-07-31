from django.conf.urls import url
from . import views

urls = [

    # Login
    url("^login/$", views.LoginView.as_view(), name="login"),
    url("^logout/$", views.logout, name="logout"),

    # Shared pages
    url("^$", views.index, name="index"),
    url("^news/$", views.index, name="news"),
    url("^courses/$", views.courses, name="courses")
]
