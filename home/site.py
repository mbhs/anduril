from django.conf.urls import url
from . import views


urls = [

    # Login
    url("^login/$", views.LoginView.as_view(), name="login"),
    url("^logout/$", views.logout, name="logout"),

    # Shared pages
    url("^$", views.IndexView.as_view(), name="index"),
    url("^news/$", views.IndexView.as_view(), name="news"),
    url("^courses/$", views.IndexView.as_view(), name="courses"),
    url("^account/$", views.IndexView.as_view(), name="account"),
    url("^profile/$", views.ProfileView.as_view(), name="profile"),

]
