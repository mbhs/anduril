"""Defines important permissions and groups.

Currently this file defines permissions that allow interface access
for administrators and alpha/beta testers.
"""

from django.contrib.auth.models import Permission, ContentType
from django.db.models.signals import pre_migrate
from django.dispatch import receiver


@receiver(pre_migrate)
def create_permissions(sender, **kwargs):
    site, _ = ContentType.objects.get_or_create(name="site", app_label="home")
    Permission.objects.get_or_create(codename="can_login", name="Can login", content_type=site)
