from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission

from core.models import User, UserProfile


class Command(BaseCommand):
    """The command to create the development users."""

    def handle(self, *args, **kwargs):
        """Run from shell."""

        User.objects.filter(username="nokim").delete()

        u = User.objects.create_user(
            username="nokim",
            type=UserProfile.STUDENT,
            profile__student_id=12345678)
        u.set_password("asdf")
        u.user_permissions.add(Permission.objects.get(codename="can_login"))
        u.is_staff = True
        u.is_superuser = True
        u.save()
