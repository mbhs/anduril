"""Models shared by other Anduril applications.

This file primarily defines user and group profile objects, which will
vary, via the polymorphism library, to serve different purposes.
"""


from django.db import models
from django.contrib.auth.models import User, Group
from polymorphic.models import PolymorphicModel


class PROFILE:
    """Profile enumeration for constants."""

    STUDENT = 0
    TEACHER = 1
    COUNSELOR = 2
    STAFF = 3
    ALUMNUS = 4

    CHOICES = (
        (STUDENT, "student"),
        (TEACHER, "teacher"),
        (COUNSELOR, "counselor"),
        (STAFF, "staff"),
        (ALUMNUS, "alumnus"))


class UserProfile(PolymorphicModel):
    """Superclass user profile model."""

    user = models.OneToOneField(User)
    type = models.IntegerField(choices=PROFILE.CHOICES)

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


class StudentProfile(UserProfile):
    """Student subclass of the user profile."""

    student_id = models.CharField(max_length=8, unique=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    counselor = models.ForeignKey(User)


class TeacherProfile(UserProfile):
    """Teacher subclass of the user profile."""

    pass


class CounselorProfile(UserProfile):
    """Counselor subclass of the user profile."""

    pass


class StaffProfile(UserProfile):
    """Staff subclass of the user profile."""

    title = models.CharField(max_length=30)
