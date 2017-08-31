from django.contrib import admin
from polymorphic import admin as polymorphic_admin

from . import models


class ClubGroupAdmin(polymorphic_admin.PolymorphicChildModelAdmin):
    base_model = models.ClubGroup


class AdministrativeGroupAdmin(polymorphic_admin.PolymorphicChildModelAdmin):
    base_model = models.AdministrativeGroup


class AcademicGroupAdmin(polymorphic_admin.PolymorphicChildModelAdmin):
    base_model = models.AcademicGroup


class ExternalGroupAdmin(polymorphic_admin.PolymorphicChildModelAdmin):
    base_model = models.ExternalGroup


class GroupAdmin(polymorphic_admin.PolymorphicParentModelAdmin):
    """Superclass group profile admin interface."""

    base_model = models.Group
    child_models = (
        models.ClubGroup,
        models.AcademicGroup,
        models.AdministrativeGroup,
        models.ExternalGroup)


# Register group admins
admin.site.register(models.ClubGroup, ClubGroupAdmin)
admin.site.register(models.AcademicGroup, AcademicGroupAdmin)
admin.site.register(models.AdministrativeGroup, AdministrativeGroupAdmin)
admin.site.register(models.ExternalGroup, ExternalGroupAdmin)
admin.site.register(models.Group, GroupAdmin)
