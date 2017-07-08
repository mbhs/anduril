"""Defines important permissions for accessing and managing groups."""

from django.contrib.auth.models import Permission, ContentType
from django.db.models.signals import pre_migrate
from django.dispatch import receiver
from core import models


@receiver(pre_migrate)
def create_permissions(sender, **kwargs):
    group, _ = ContentType.objects.get_for_model(models.Group)
    Permission.objects.get_or_create(codename="can_manage_groups", name="Can login", content_type=group)
