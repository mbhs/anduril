from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission

import getpass

from core.models import User, UserProfile


class Command(BaseCommand):
    """Conveniently create users for development."""

    def handle(self, *args, **kwargs):
        """Run from shell."""

        username = input("Username: ")
        student_id = int(input("Student ID: "))
        password = getpass.getpass("Password: ")

        User.objects.filter(username=username).delete()

        u = User.objects.create_user(
            username=username,
            type=UserProfile.STUDENT,
            profile__student_id=student_id)
        u.set_password(password)
        u.user_permissions.add(Permission.objects.get(codename="can_login"))
        u.is_staff = True
        u.is_superuser = True
        u.save()
