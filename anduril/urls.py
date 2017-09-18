"""anduril URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
import home.site
import api.site
import groups.site


urlpatterns = [
    url(r"", include(home.site.urls, namespace="home")),
    url(r"^groups/", include(groups.site.urls, namespace="groups")),
    url(r"^api/", include(api.site.urls, namespace="api")),
    url(r"^admin/", admin.site.urls),
    url(r"^oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    url(r'^openid/', include('oidc_provider.urls', namespace='oidc_provider')),
]
