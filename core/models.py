"""Models shared by other Anduril applications.

This file primarily defines user and group profile objects, which vary,
via the polymorphic library, to serve as different types of each.
"""

from django.db import models
from polymorphic.models import PolymorphicModel
from django.contrib.auth import models as auth
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save, pre_delete
from django.db.models.fields import related_descriptors
from django.dispatch import receiver
from django.utils import timezone

from lib.models import TimeTrackingModel


class UserManager(auth.UserManager):
    """User manager that modifies create for polymorphic profiles.
    
    A separate user manager is necessary to override User object
    create. Since we want to avoid any situations where a user
    object doesn't have a profile, we require it as a parameter.
    """

    def create_user(self, username, email=None, password=None, type: str=None, **extra_fields):
        """Create a user with an enumerated user profile type."""

        profile_fields = {}
        for field in tuple(extra_fields):
            if field.startswith("profile__"):
                profile_field = field[len("profile__"):]
                profile_fields[profile_field] = extra_fields.pop(field)

        user = User(username=username, **extra_fields)
        user.save()

        # Must be created here to use profile data
        profile = UserProfile.concrete[type](user=user, **profile_fields)
        profile.save()

        user.save()
        return user


class User(auth.User):
    """User proxy that overrides user create."""

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

    @property
    def slug(self):
        """Get the URL slug of the model."""

        return f"/users/{self.id}"


@receiver(post_save, sender=User)
def on_create_user(sender, instance, created, **kwargs):
    """Add members to the user when it is created."""

    if not created:
        return

    # User profile is created manually
    UserStatistics.objects.create(user=instance)


@receiver(post_save, sender=User)
def on_save_user(sender, instance, **kwargs):
    """Save the corresponding profile when the user is saved."""

    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        pass

    try:
        instance.statistics.save()
    except UserStatistics.DoesNotExist:
        pass


class UserProfile(PolymorphicModel, TimeTrackingModel):
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

    def __init__(self, *args, **kwargs):
        """Initialize a user profile."""

        if "user" in kwargs:
            kwargs["user_id"] = kwargs["user"].id
        super().__init__(*args, **kwargs)

    # Actual profile fields
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    type = ABSTRACT

    middle_name = models.CharField(blank=True, null=True, max_length=60)
    display_first_name = models.CharField(blank=True, null=True, max_length=60)
    display_last_name = models.CharField(blank=True, null=True, max_length=60)

    @property
    def slug(self):
        """Get the URL slug of the model."""

        return self.user.slug

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


class UserStatistics(models.Model):
    """User statistics object.
    
    This is here to collect arbitrary bits of data about site usage, 
    including login counts, first join date, etc.
    """

    user = models.OneToOneField(User, related_name="statistics", on_delete=models.CASCADE)
    first_login = models.DateTimeField(blank=True, null=True)
    login_count = models.IntegerField(default=0)

    def __repr__(self):
        """Represent the container as a string."""

        return f"<Statistics for {self.user.get_full_name()}>"


@receiver(user_logged_in)
def update_user_login_statistics(sender, user, request, **kwargs):
    """Called when a user logs into the system."""

    try:
        if user.statistics.login_count == 0:
            user.statistics.first_login = timezone.now()
        user.statistics.login_count += 1
        user.statistics.save()
    except UserStatistics.DoesNotExist:
        pass


@UserProfile.register(UserProfile.STUDENT)
class StudentUserProfile(UserProfile):
    """Student subclass of the user profile."""

    student_id = models.CharField(max_length=8, unique=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    counselor = models.ForeignKey(User, blank=True, null=True)


@UserProfile.register(UserProfile.TEACHER)
class TeacherUserProfile(UserProfile):
    """Teacher subclass of the user profile."""


@UserProfile.register(UserProfile.COUNSELOR)
class CounselorUserProfile(UserProfile):
    """Counselor subclass of the user profile."""


@UserProfile.register(UserProfile.STAFF)
class StaffUserProfile(UserProfile):
    """Staff subclass of the user profile."""

    title = models.CharField(max_length=30)


@UserProfile.register(UserProfile.ALUMNUS)
class AlumnusUserProfile(UserProfile):
    """Staff subclass of the user profile."""

    graduation_year = models.IntegerField(blank=True, null=True)
