"""Models for site management.

The sites app will be a convenient way to manage multiple aspects of
web hosting, including DNS, internal configuration, and file hosting.
As such, models here will naively wrap features present in other 
software.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

import string


URL_SAFE_CHARACTERS = string.ascii_letters + string.digits + "_-"


def is_url_safe(s: str) -> bool:
    """Check if a string contains only safe characters."""

    for c in s:
        if c not in URL_SAFE_CHARACTERS:
            return False
    return True


class URLSafeField(models.CharField):
    """Character field that only allows URL-safe characters."""

    default_validators = [is_url_safe]
    description = _("Component of a URL.")


class Url(models.Model):
    """A base URL owned by the hosting organization."""

    url = models.URLField(_("URL"))
    site = models.ForeignKey("Site")


class SubdomainUrl(models.Model):
    """Subdomain URL that references a base URL."""

    base = models.ForeignKey(Url, name=_("Base URL"), related_name="subdomains")
    head = URLSafeField(max_length=50)


class Site(models.Model):
    """Represent a site hosted on the host website."""
