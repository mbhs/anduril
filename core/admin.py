"""Administrative interface managers for core models.

Because we're using polymorphic models, we have to put a little bit 
more work into how the admin wrappers work.
"""

from django.contrib import admin
from polymorphic import admin as polymorphic_admin
from django.contrib.auth import admin as auth_admin
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User, Group
from . import models


class UserProfileInline(polymorphic_admin.StackedPolymorphicInline):
    """User profile inline form for the User admin interface."""

    class StudentUserProfileInline(polymorphic_admin.StackedPolymorphicInline.Child):
        model = models.StudentUserProfile

    class TeacherUserProfileInline(polymorphic_admin.StackedPolymorphicInline.Child):
        model = models.TeacherUserProfile

    class CounselorUserProfileInline(polymorphic_admin.StackedPolymorphicInline.Child):
        model = models.CounselorUserProfile

    class StaffUserProfileInline(polymorphic_admin.StackedPolymorphicInline.Child):
        model = models.StaffUserProfile

    class AlumnusUserProfileInline(polymorphic_admin.StackedPolymorphicInline.Child):
        model = models.AlumnusUserProfile

    model = models.UserProfile
    child_inlines = (StudentUserProfileInline,)

    fk_name = "user"
    can_delete = False
    verbose_name_plural = "Profile"


class UserCreationForm(auth_forms.UserCreationForm):
    """Add fields to user creation to support profile type."""

    type = forms.ChoiceField(models.USER.TYPES)

    def save(self, commit=True):
        """Save the user form."""

        type = self.cleaned_data.get("type")
        user = super().save(commit=False)
        models.User.objects.create_profile(user, type)
        user.save()

    class Meta:
        model = models.User
        fields = "__all__"


class UserAdmin(polymorphic_admin.PolymorphicInlineSupportMixin, auth_admin.UserAdmin):
    """Superclass user profile inline form."""

    # http://stackoverflow.com/a/23337009/3015219
    form = UserCreationForm
    add_fieldsets = ((None, {"fields": ("username", "type", "password1", "password2")}),)

    inlines = (UserProfileInline,)



admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(models.User, UserAdmin)
