"""Models shared by other Anduril applications.

This file primarily defines user and group profile objects, which vary,
via the polymorphic library, to serve as different types of each.
"""

from django.db import models
from polymorphic.models import PolymorphicModel
from django.contrib.auth import models as auth
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class USER:
    """User profile enumeration and registration."""

    DEFAULT = None
    STUDENT = "student"
    TEACHER = "teacher"
    COUNSELOR = "counselor"
    STAFF = "staff"
    ALUMNUS = "alumnus"

    TYPES = [STUDENT, TEACHER, COUNSELOR, STAFF, ALUMNUS]

    choices = map(lambda x: (x, x.capitalize()), TYPES)

    models = {}

    @staticmethod
    def register(type):
        """Register a profile class to a user enumeration."""

        def _register(cls):
            USER.models[type] = cls
            cls.type = type
            return cls
        return _register


class UserManager(auth.UserManager):
    """User manager that modifies creation for polymorphic profiles.
    
    A separate user manager is necessary to override User object
    creation. Since we want to avoid any situations where a user 
    object doesn't have a profile, we require it as a parameter.
    """

    def create_user(self, username, email=None, password=None, type: USER=None, **extra_fields):
        """Create a user with an enumerated user profile type."""

        profile_fields = {}
        for field in tuple(extra_fields):
            if field.startswith("profile__"):
                profile_field = field[len("profile__"):]
                profile_fields[profile_field] = extra_fields.pop(field)

        user = User(**extra_fields)
        profile = USER.models[type](user=user, **profile_fields)
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

    user = models.OneToOneField(User, related_name="profile")
    type = USER.DEFAULT

    middle_name = models.CharField(blank=True, null=True, max_length=60)
    display_first_name = models.CharField(blank=True, null=True, max_length=60)
    display_last_name = models.CharField(blank=True, null=True, max_length=60)

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


@USER.register(USER.STUDENT)
class StudentUserProfile(UserProfile):
    """Student subclass of the user profile."""

    student_id = models.CharField(max_length=8, unique=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    counselor = models.ForeignKey(User, blank=True, null=True)


@USER.register(USER.TEACHER)
class TeacherUserProfile(UserProfile):
    """Teacher subclass of the user profile."""


@USER.register(USER.COUNSELOR)
class CounselorUserProfile(UserProfile):
    """Counselor subclass of the user profile."""


@USER.register(USER.STAFF)
class StaffUserProfile(UserProfile):
    """Staff subclass of the user profile."""

    title = models.CharField(max_length=30)


@USER.register(USER.ALUMNUS)
class AlumnusUserProfile(UserProfile):
    """Staff subclass of the user profile."""

    graduation_year = models.IntegerField(blank=True, null=True)


class GROUP:
    """Group profile enumeration and registration."""

    DEFAULT = None
    CLUB = "club"
    ACADEMIC = "academic"

    models = {}

    @staticmethod
    def register(type):
        """Register a profile class to a group enumeration."""

        def _register(cls):
            GROUP.models[type] = cls
            cls.type = type
            return cls
        return _register


class GroupManager(auth.GroupManager):
    """User manager that modifies creation for polymorphic profiles."""

    def create(self, type: GROUP, **options):
        """Create a group with an enumerated group profile type."""

        profile_options = {}
        for option in tuple(options):
            if option.startswith("profile__"):
                profile_options[option] = options.pop(option)

        group = super().create(**options)
        profile = GROUP.models[type].objects.create(group=group, **profile_options)
        profile.save()
        return group


class Group(auth.Group):
    """Group proxy that overrides user creation"""

    objects = GroupManager()

    class Meta:
        proxy = True

    def __repr__(self):
        """Represent the group as a string."""

        try:
            return f"<Group.{self.profile.type.capitalize()} {self.name}>"
        except AttributeError:
            return f"<Group {self.name}>"

    __str__ = __repr__


@receiver(post_save, sender=Group)
def save_group_profile(sender, instance, **kwargs):
    """Save the corresponding profile when the group is saved."""

    # TODO: test groups, this line might not be necessary
    instance.profile.group_id = instance.id
    instance.profile.save()


@receiver(pre_delete, sender=Group)
def delete_group_profile(sender, instance, **kwargs):
    """Delete the group profile prior to group deletion."""

    try:
        instance.profile.delete()
    except Exception as e:
        print(f"Failed to delete user profile: {e}")


class GroupProfile(PolymorphicModel):
    """Superclass group profile model."""

    group = models.OneToOneField(Group, related_name="profile")

    title = models.CharField(max_length=80)
    description = models.CharField(max_length=160)


@USER.register(GROUP.CLUB)
class ClubGroupProfile(GroupProfile):
    """Type of group used for extracurricular clubs."""

    sponsor = models.ManyToManyField(User)


@USER.register(GROUP.ACADEMIC)
class AcademicGroupProfile(GroupProfile):
    """Academic organization profile."""
