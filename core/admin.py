"""Administrative interface managers for core models.

Because we're using polymorphic models, we have to put a little bit
more work into how the admin wrappers work.
"""

from django.contrib import admin
from polymorphic import admin as polymorphic_admin
from django.contrib.auth import admin as auth_admin
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import validators as auth_validators
from django.contrib.auth.models import User, Group, Permission
from . import models
from . import rules


USERNAME_HELP_TEXT = """\
<ul>\
<li>150 characters or fewer. Letters, digits and @/./+/-/_ only.</li>\
<li>Username will be auto-generated if left blank.</li>\
</ul>
"""


class UserProfileInline(polymorphic_admin.StackedPolymorphicInline):
    """User profile inline form for the User admin interface."""

    class StudentUserProfileInline(polymorphic_admin.StackedPolymorphicInline.Child):
        verbose_name = "Student user profile"
        model = models.StudentUserProfile

    class TeacherUserProfileInline(polymorphic_admin.StackedPolymorphicInline.Child):
        verbose_name = "Teacher user profile"
        model = models.TeacherUserProfile

    class CounselorUserProfileInline(polymorphic_admin.StackedPolymorphicInline.Child):
        verbose_name = "Counselor user profile"
        model = models.CounselorUserProfile

    class StaffUserProfileInline(polymorphic_admin.StackedPolymorphicInline.Child):
        verbose_name = "Staff user profile"
        model = models.StaffUserProfile

    class AlumnusUserProfileInline(polymorphic_admin.StackedPolymorphicInline.Child):
        verbose_name = "Alumnus user profile"
        model = models.AlumnusUserProfile

    model = models.UserProfile
    child_inlines = (
        StudentUserProfileInline,
        TeacherUserProfileInline,
        CounselorUserProfileInline,
        StaffUserProfileInline,
        AlumnusUserProfileInline)

    max_num = 1
    extra = 0

    fk_name = "user"
    can_delete = True
    verbose_name_plural = "Profile"


class GroupProfileInline(polymorphic_admin.StackedPolymorphicInline):
    """User profile inline form for the User admin interface."""

    class AcademicGroupProfileInline(polymorphic_admin.StackedPolymorphicInline.Child):
        verbose_name = "Academic group profile"
        model = models.AcademicGroupProfile

    class ClubGroupProfileInline(polymorphic_admin.StackedPolymorphicInline.Child):
        verbose_name = "Club group profile"
        model = models.ClubGroupProfile

    class OrganizationGropuProfileInline(polymorphic_admin.StackedPolymorphicInline.Child):
        verbose_name = "Organization group profile"
        model = models.OrganizationGroupProfile

    model = models.GroupProfile
    child_inlines = (
        AcademicGroupProfileInline,
        ClubGroupProfileInline,
        OrganizationGropuProfileInline)

    max_num = 1
    extra = 0

    fk_name = "group"
    can_delete = True
    verbose_name_plural = "Profile"


class OptionalUnicodeUsernameValidator(auth_validators.UnicodeUsernameValidator):
    """Only check username conditions if admin has entered a value."""

    def __call__(self, value):
        """Call the validator on the value if not whitespace."""

        if value.strip():
            return super(OptionalUnicodeUsernameValidator, self).__call__(value)


class UserCreationForm(auth_forms.UserCreationForm):
    """Add fields to user creation to support profile type."""

    username = auth_forms.UsernameField(
        required=False,
        strip=True,
        max_length=150,
        validators=[OptionalUnicodeUsernameValidator],
        help_text=USERNAME_HELP_TEXT)

    def clean_username(self):
        """Return the cleaned or auto-generated username."""

        username = self.cleaned_data.get("username")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        if not username:
            if not first_name or not last_name:
                raise forms.ValidationError("Username generation requires first and last name.")
            username_generator = rules.generate_username(first_name, last_name)
            username = next(username_generator)
            while models.User.objects.filter(username=username).exists():
                username = next(username_generator)
        return username

    class Meta:
        model = models.User
        fields = ("email", "first_name", "last_name")


class UserAdmin(polymorphic_admin.PolymorphicInlineSupportMixin, auth_admin.UserAdmin):
    """Superclass user profile admin interface."""

    add_form = UserCreationForm
    add_fieldsets = ((None, {"fields": ("first_name", "last_name", "username", "email", "password1", "password2")}),)

    inlines = (UserProfileInline,)


class GroupAdmin(polymorphic_admin.PolymorphicInlineSupportMixin, auth_admin.GroupAdmin):
    """Superclass group profile admin interface."""

    inlines = (GroupProfileInline,)


# Register the new user and group admin
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Group, GroupAdmin)
admin.site.register(Permission)
