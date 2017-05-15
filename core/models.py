"""Models shared by other Anduril applications.

This file primarily defines user and group profile objects, which will
vary, via the polymorphism library, to serve different purposes.
"""

from django.db import models
from django.contrib.auth import models as auth
from polymorphic.models import PolymorphicModel


class PROFILE:
    """User profile enumeration."""

    DEFAULT = None
    STUDENT = "student"
    TEACHER = "teacher"
    COUNSELOR = "counselor"
    STAFF = "staff"
    ALUMNUS = "alumnus"


class GROUP:
    """Group profile enumeration."""

    DEFAULT = None
    CLUB = "club"
    ACADEMIC = "academic"


class UserManager(auth.UserManager):
    """User manager that overrides user creation for polymorphic."""

    def create(self, type, username, email=None, password=None, **extra_fields):
        """Create a user with an enumerated type."""

        user = super().create(username, email, password, **extra_fields)
        user.profile = {
            PROFILE.DEFAULT: UserProfile,
            PROFILE.STUDENT: StudentUserProfile,
            PROFILE.TEACHER: TeacherUserProfile,
            PROFILE.COUNSELOR: CounselorUserProfile,
            PROFILE.STAFF: StaffUserProfile,
            PROFILE.ALUMNUS: AlumnusUserProfile
        }[type].objects.create(user=user, **extra_fields.get("profile", {}))


class User(auth.User):
    """User proxy to allow polymorphic profiles."""

    objects = UserManager()

    class Meta:
        proxy = True


class UserProfile(PolymorphicModel):
    """Superclass user profile model."""

    user = models.OneToOneField(User)
    type = PROFILE.DEFAULT

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


class StudentUserProfile(UserProfile):
    """Student subclass of the user profile."""

    type = PROFILE.STUDENT

    student_id = models.CharField(max_length=8, unique=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    counselor = models.ForeignKey(User)


class TeacherUserProfile(UserProfile):
    """Teacher subclass of the user profile."""

    type = PROFILE.TEACHER


class CounselorUserProfile(UserProfile):
    """Counselor subclass of the user profile."""

    type = PROFILE.COUNSELOR


class StaffUserProfile(UserProfile):
    """Staff subclass of the user profile."""

    type = PROFILE.STAFF
    title = models.CharField(max_length=30)


class AlumnusUserProfile(UserProfile):
    """Staff subclass of the user profile."""

    type = PROFILE.ALUMNUS
    graduation_year = models.IntegerField(blank=True, null=True)


class GroupProfile(PolymorphicModel):
    """Superclass group profile model."""

    group = models.OneToOneField(Group, related_name="profile")
    type = GROUP.ACADEMIC

    title = models.CharField(max_length=80)
    description = models.CharField(max_length=160)


class ClubGroupProfile(GroupProfile):
    """Type of group used for extracurricular clubs."""

    type = GROUP.CLUB
    sponsor = models.ManyToManyField(User)


class AcademicGroupProfile(GroupProfile):
    """Academic organization profile."""

    type = GROUP.ACADEMIC
