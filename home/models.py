from django.db import models
from django.contrib.auth.models import Permission, ContentType

from core.models import User, Organization, TimeTrackingModel


class Friendship(TimeTrackingModel):
    """A friendship between two users."""

    a = models.ForeignKey(User, related_name="+")
    b = models.ForeignKey(User, related_name="+")
    confirmed = models.BooleanField(default=False)

    @staticmethod
    def between(a, b) -> bool:
        """Check if two users are friends."""

        return (Friendship.objects.filter(a=a, b=b, confirmed=True) |
                Friendship.objects.filter(a=b, b=a, confirmed=True)).first()

    @staticmethod
    def friends(user, confirmed=True) -> list:
        """Get all friends of a user."""

        ids = (set(Friendship.objects.filter(a=user, confirmed=confirmed).values_list("b", flat=True)) |
               set(Friendship.objects.filter(b=user, confirmed=confirmed).values_list("a", flat=True)))
        return User.objects.filter(pk__in=ids)


class Permissions(models.Model):
    """Permissions container not managed in the database."""

    class Meta:
        managed = False
        permissions = (
            ("can_login", "Can login to home"),)
