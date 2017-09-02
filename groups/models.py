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
            ("can_manage_groups", "Can manage groups"),
            ("can_request_group", "Can submit group application"),)

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
    """Group for clubs at Blair."""

    about = """Club groups are for organized extracurricular 
    activities hosted at Blair, and include sports, academic, and 
    hobby groups. Club groups require a teacher or staff sponsor and
    must be approved by the club administrator at Blair."""

    sponsor = models.ManyToManyField(User)


@Group.register(Group.ACADEMIC)
class AcademicGroup(Group):
    """Group for teachers and staff to communicate with students."""

    about = """Academic groups are largely reserved for teachers, 
    staff, and administrators at Blair. They provide a means of 
    communication with students, and can serve as a platform for 
    organizing school events."""


@Group.register(Group.ADMINISTRATIVE)
class AdministrativeGroup(Group):
    """Administrative organization."""

    about = """Blah blah blah."""


@Group.register(Group.EXTERNAL)
class ExternalGroup(Group):
    """Generic organization profile."""

    about = """Blah blah blah blah."""
