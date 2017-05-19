from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin
import polymorphic.admin
from django.core.urlresolvers import reverse
from . import models


class UserAdmin(admin.ModelAdmin):
    """Modified user administrative interface."""

    list_display = ["username", "first_name", "last_name", "profile"]

    def profile(self, obj):
        """Get the type of user from its profile."""

        try:
            profile = obj.profile
            url = reverse(f"admin:{obj._meta.app_label}_{obj._meta.model_name}", args=[obj.id])
            return f"""<a href="{url}">{profile.type.capitalize()}</a>"""
        except AttributeError:
            return "None"


class UserProfileAdmin(polymorphic.admin.PolymorphicParentModelAdmin):
    """Parent class user profile administrative interface."""

    base_model = models.UserProfile

    def get_child_models(self):
        """Get the child models."""

        pass


#admin.site.register(models.User, UserAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
