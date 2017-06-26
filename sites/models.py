"""Models for site management.

The sites app will be a convenient way to manage multiple aspects of
web hosting, including DNS, internal configuration, and file hosting.
As such, models here will naively wrap features present in other 
software.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _


class URLSafeField(models.CharField):
    """Character field that only allows URL-safe characters."""


class Url(models.Model):
    """A base URL owned by the hosting organization."""

    url = models.URLField(_("URL"))


class SubdomainUrl(models.Model):
    """Subdomain URL that references a base URL."""

    base = models.ForeignKey(Url, name=_("Base URL"), related_name="subdomains")
    head = URLSafeField(max_length=50)
