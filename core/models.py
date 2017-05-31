"""Models shared by other Anduril applications.

This file primarily defines user and group profile objects, which vary,
via the polymorphic library, to serve as different types of each.
"""

from django.db import models
from polymorphic.models import PolymorphicModel
from django.contrib.auth import models as auth
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


class UserManager(auth.UserManager):
    """User manager that modifies creation for polymorphic profiles.
    
    A separate user manager is necessary to override User object
    creation. Since we want to avoid any situations where a user 
    object doesn't have a profile, we require it as a parameter.
    """

    def create_user(self, username, email=None, password=None, type: str=None, **extra_fields):
        """Create a user with an enumerated user profile type."""

        profile_fields = {}
        for field in tuple(extra_fields):
            if field.startswith("profile__"):
                profile_field = field[len("profile__"):]
                profile_fields[profile_field] = extra_fields.pop(field)

        user = User(**extra_fields)
        profile = UserProfile.concrete[type](user=user, **profile_fields)
        profile.user_id = user.id
        user.save()
        return user


class User(auth.User):
    """User proxy that overrides user creation."""

    objects = UserManager()

    class Meta:
        proxy = True

    def __repr__(self):
        """Represent the user as a string."""

        try:
            return f"<User.{self.profile.type.capitalize()} {self.username}>"
        except AttributeError:
            return f"<User {self.username}>"

    __str__ = __repr__


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the corresponding profile when the user is saved."""

    instance.profile.user_id = instance.id  # TODO: figure out why this is necessary
    instance.profile.save()


@receiver(pre_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    """Delete the user profile prior to user deletion."""

    try:
        instance.profile.delete()
    except Exception as e:
        print("Failed to delete user profile:", e)


class UserProfile(PolymorphicModel):
    """Base user profile model."""

    # Enumerated profile types
    ABSTRACT = None
    STUDENT = "student"
    TEACHER = "teacher"
    COUNSELOR = "counselor"
    STAFF = "staff"
    ALUMNUS = "alumnus"

    TYPES = [STUDENT, TEACHER, COUNSELOR, STAFF, ALUMNUS]
    choices = map(lambda x: (x, x.capitalize()), TYPES)
    concrete = {}

    @staticmethod
    def register(type):
        """Register a profile class to a user enumeration."""

        def _register(cls):
            UserProfile.concrete[type] = cls
            cls.type = type
            return cls
        return _register

    # Actual profile fields
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    type = ABSTRACT

    middle_name = models.CharField(blank=True, null=True, max_length=60)
    display_first_name = models.CharField(blank=True, null=True, max_length=60)
    display_last_name = models.CharField(blank=True, null=True, max_length=60)

    # Meta
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    @property
    def first_name(self):
        """Get the display first or first name of the user."""

        return self.display_first_name or self.user.first_name

    @property
    def last_name(self):
        """Get the display first or first name of the user."""

        return self.display_last_name or self.user.last_name

    @property
    def full_name(self):
        """Get the full name of the user."""

        return self.first_name + " " + self.last_name


@UserProfile.register(UserProfile.STUDENT)
class StudentUserProfile(UserProfile):
    """Student subclass of the user profile."""

    student_id = models.CharField(_("student id"), max_length=8, unique=True)
    graduation_year = models.IntegerField(_("graduation year"), blank=True, null=True)
    counselor = models.ForeignKey(User, verbose_name=_("counselor"), blank=True, null=True)

    # Meta
    class Meta:
        verbose_name = _('student profile')
        verbose_name_plural = _('student profiles')


@UserProfile.register(UserProfile.TEACHER)
class TeacherUserProfile(UserProfile):
    """Teacher subclass of the user profile."""

    # Meta
    class Meta:
        verbose_name = _('teacher profile')
        verbose_name_plural = _('teacher profiles')


@UserProfile.register(UserProfile.COUNSELOR)
class CounselorUserProfile(UserProfile):
    """Counselor subclass of the user profile."""

    # Meta
    class Meta:
        verbose_name = _('counselor profile')
        verbose_name_plural = _('counselor profiles')


@UserProfile.register(UserProfile.STAFF)
class StaffUserProfile(UserProfile):
    """Staff subclass of the user profile."""

    title = models.CharField(_("title"), max_length=30)

    # Meta
    class Meta:
        verbose_name = _('staff profile')
        verbose_name_plural = _('staff profiles')


@UserProfile.register(UserProfile.ALUMNUS)
class AlumnusUserProfile(UserProfile):
    """Staff subclass of the user profile."""

    graduation_year = models.IntegerField(_("graduation year"), blank=True, null=True)

    # Meta
    class Meta:
        verbose_name = _('alumnus profile')
        verbose_name_plural = _('alumnus profiles')


class GroupMembership(models.Model):
    """Represents group membership with added functionality."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    roles = models.CharField(max_length=30)
    join_time = models.DateTimeField()


class Group(PolymorphicModel):
    """Group base class.
    
    While the user model proxies the existing django user class in
    order to utilize existing authentication, there are several 
    features of groups that make it desirable to define them as a
    standalone model. For example, members will have roles, which will
    be stored in an intermediate membership model.
    """

    # Enumerated group types
    ABSTRACT = None
    CLUB = "club"
    ACADEMIC = "academic"
    ORGANIZATION = "organization"
    concrete = {}

    @staticmethod
    def register(type):
        """Register a profile class to a group enumeration."""

        def _register(cls):
            Group.concrete[type] = cls
            cls.type = type
            return cls
        return _register

    # Actual group fields
    name = models.CharField(_("name"), max_length=80, unique=True)
    users = models.ManyToManyField(User, verbose_name=_("users"), through=GroupMembership)

    title = models.CharField(max_length=80)
    description = models.CharField(max_length=160)

    type = ABSTRACT

    # Meta
    class Meta:
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    def __repr__(self):
        """Represent the group as a string."""

        try:
            return f"<Group.{self.type.capitalize()} {self.name}>"
        except AttributeError:
            return f"<Group {self.name}>"

    __str__ = __repr__


@Group.register(Group.CLUB)
class ClubGroup(Group):
    """Type of group used for extracurricular clubs."""

    sponsor = models.ManyToManyField(User)


@Group.register(Group.ACADEMIC)
class AcademicGroup(Group):
    """Academic organization profile."""


@Group.register(Group.ORGANIZATION)
class OrganizationGroup(Group):
    """Generic organization profile."""
