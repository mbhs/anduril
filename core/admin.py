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
from polymorphic import formsets as polymorphic_forms
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe
from . import models
from . import rules


class UserProfileInlineFormSet(polymorphic_forms.BasePolymorphicInlineFormSet):
    """Required user profile formset."""

    def _construct_form(self, i, **kwargs):
        """Require a profile object on instantiation."""

        form = super()._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form


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
    child_inlines = (
        StudentUserProfileInline,
        TeacherUserProfileInline,
        CounselorUserProfileInline,
        StaffUserProfileInline,
        AlumnusUserProfileInline)

    formset = UserProfileInlineFormSet
    max_num = 1

    fk_name = "user"
    can_delete = False
    verbose_name_plural = "Profile"


class OptionalUnicodeUsernameValidator(auth_validators.UnicodeUsernameValidator):
    """Only check username conditions if admin has entered a value."""

    def __call__(self, value):
        """Call the validator on the value if not whitespace."""

        if value.strip():
            return super().__call__(value)


class UserCreationForm(auth_forms.UserCreationForm):
    """Add fields to user creation to support profile type."""

    username = auth_forms.UsernameField(
        required=False,
        strip=True,
        max_length=150,
        validators=[OptionalUnicodeUsernameValidator],
        help_text=mark_safe("<ul><li>150 characters or fewer. Letters, digits and @/./+/-/_ only.</li>"
                            "<li>Username will be auto-generated if left blank.</li></ul>"))

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
    """Superclass user profile inline form."""

    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            "fields": ("first_name", "last_name", "username", "email", "password1", "password2")
        }),)

    inlines = (UserProfileInline,)


# Register the new user and group admin
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(models.User, UserAdmin)
