"""Defines important permissions and groups.

Currently this file defines permissions that allow interface access
for administrators and alpha/beta testers.
"""

from django.contrib.auth.models import Permission, ContentType


site, _ = ContentType.objects.get_or_create(name="site", app_label="home")
Permission.objects.get_or_create(codename="can_login", name="Can login", content_type=site)
