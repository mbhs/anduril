from django.db import models
from polymorphic.models import PolymorphicModel

from core.models import User
from lib.models import TimeTrackingModel


class GroupMembership(TimeTrackingModel):
    """Represents group membership with added functionality."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE)
    roles = models.CharField(max_length=30)


class Group(PolymorphicModel, TimeTrackingModel):
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
    ADMINISTRATIVE = "administrative"
    EXTERNAL = "external"
    concrete = {}

    @staticmethod
    def register(group):
        """Register a group type to an enumeration."""

        def _register(cls):
            Group.concrete[group] = cls
            cls.type = group
            return cls
        return _register

    # Actual group fields
    name = models.CharField(max_length=80, unique=True)
    users = models.ManyToManyField(User, through=GroupMembership, related_name="organizations")
    title = models.CharField(max_length=80)
    description = models.TextField()

    # Whether the group is hidden
    hidden = models.BooleanField()

    type = ABSTRACT

    # Meta
    class Meta:
        permissions = (
            ("can_manage_groups", "Can manage groups"),)

    def __repr__(self):
        """Represent the group as a string."""

        try:
            return f"<Group.{self.type.capitalize()} {self.name}>"
        except AttributeError:
            return f"<Group {self.name}>"

    __str__ = __repr__

    @property
    def slug(self):
        """Get the URL slug of the model."""

        return f"/groups/{self.id}"


@Group.register(Group.CLUB)
class ClubGroup(Group):
    """Type of group used for extracurricular clubs."""

    sponsor = models.ManyToManyField(User)


@Group.register(Group.ACADEMIC)
class AcademicGroup(Group):
    """Academic organization profile."""


@Group.register(Group.ADMINISTRATIVE)
class AdministrativeGroup(Group):
    """Administrative organization."""


@Group.register(Group.EXTERNAL)
class ExternalGroup(Group):
    """Generic organization profile."""
