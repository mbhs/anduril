"""Models shared by other Anduril applications.

This file primarily defines user and group profile objects, which will
vary, via the polymorphism library, to serve different purposes.
"""

from django.db import models
from polymorphic.models import PolymorphicModel
from django.contrib.auth import models as auth
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class USER:
    """User profile enumeration."""

    DEFAULT = None
    STUDENT = "student"
    TEACHER = "teacher"
    COUNSELOR = "counselor"
    STAFF = "staff"
    ALUMNUS = "alumnus"

    models = {}

    @staticmethod
    def register(type):
        """Register a profile."""

        def _register(cls):
            USER.models[type] = cls
            return cls
        return _register


class UserManager(auth.UserManager):
    """User manager that overrides user creation for polymorphic."""

    def create(self, type: USER, **options):
        """Create a user with an enumerated type."""

        profile_options = {}
        for option in tuple(options):
            if option.startswith("profile__"):
                profile_option = option[len("profile__"):]
                profile_options[profile_option] = options.pop(option)

        user = User(**options)
        profile = USER.models[type](user=user, **profile_options)
        profile.user_id = user.id
        user.save()
        return user


class User(auth.User):
    """User proxy to allow polymorphic profiles."""

    objects = UserManager()

    class Meta:
        proxy = True

    def __repr__(self):
        """Represent the user as a string."""

        try:
            return f"<{self.profile.type.capitalize()} {self.username}>"
        except AttributeError:
            return f"<User {self.username}>"

    __str__ = __repr__


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the corresponding profile when the user is saved."""

    # TODO: figure out why this isn't working
    instance.profile.user_id = instance.id
    instance.profile.save()


@receiver(pre_delete, sender=User)
def delete_user_profile(sender, instance, **kwargs):
    """Delete the user profile prior to user deletion."""

    try:
        instance.profile.delete()
    except Exception as e:
        print("Failed to delete user profile:", e)


class UserProfile(PolymorphicModel):
    """Superclass user profile model."""

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


@USER.register(USER.STUDENT)
class StudentUserProfile(UserProfile):
    """Student subclass of the user profile."""

    type = USER.STUDENT

    student_id = models.CharField(max_length=8, unique=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    counselor = models.ForeignKey(User, blank=True, null=True)


@USER.register(USER.TEACHER)
class TeacherUserProfile(UserProfile):
    """Teacher subclass of the user profile."""

    type = USER.TEACHER


@USER.register(USER.COUNSELOR)
class CounselorUserProfile(UserProfile):
    """Counselor subclass of the user profile."""

    type = USER.COUNSELOR


@USER.register(USER.STAFF)
class StaffUserProfile(UserProfile):
    """Staff subclass of the user profile."""

    type = USER.STAFF
    title = models.CharField(max_length=30)


@USER.register(USER.ALUMNUS)
class AlumnusUserProfile(UserProfile):
    """Staff subclass of the user profile."""

    type = USER.ALUMNUS
    graduation_year = models.IntegerField(blank=True, null=True)


class GROUP:
    """Group profile enumeration."""

    DEFAULT = None
    CLUB = "club"
    ACADEMIC = "academic"

    models = {}

    @staticmethod
    def register(type):
        """Register a profile."""

        def _register(cls):
            GROUP.models[type] = cls
            return cls
        return _register


class GroupManager(auth.GroupManager):
    """User manager that overrides user creation for polymorphic."""

    def create(self, type: GROUP, **options):
        """Create a user with an enumerated type."""

        profile_options = {}
        for option in tuple(options):
            if option.startswith("profile__"):
                profile_options[option] = options.pop(option)

        group = super().create(**options)
        profile = GROUP.models[type].objects.create(group=group, **profile_options)
        profile.save()
        return group


class Group(auth.Group):
    """User proxy to allow polymorphic profiles."""

    objects = GroupManager()

    class Meta:
        proxy = True

    def __repr__(self):
        """Represent the user as a string."""

        try:
            return f"<{self.profile.type.capitalize()} {self.name}>"
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
        print("Failed to delete user profile:", e)


class GroupProfile(PolymorphicModel):
    """Superclass group profile model."""

    group = models.OneToOneField(Group, related_name="profile")
    type = GROUP.ACADEMIC

    title = models.CharField(max_length=80)
    description = models.CharField(max_length=160)


@USER.register(GROUP.CLUB)
class ClubGroupProfile(GroupProfile):
    """Type of group used for extracurricular clubs."""

    type = GROUP.CLUB
    sponsor = models.ManyToManyField(User)


@USER.register(GROUP.ACADEMIC)
class AcademicGroupProfile(GroupProfile):
    """Academic organization profile."""

    type = GROUP.ACADEMIC
