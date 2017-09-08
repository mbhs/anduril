from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

import os

from anduril.settings import BASE_DIR


class Command(BaseCommand):
    """Conveniently create users for development."""

    def handle(self, *args, **kwargs):
        """Run from shell."""

        allowed_chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        with open(os.path.join(BASE_DIR, "anduril", "settings", "secret.py"), "w") as file:
            file.write(f"""SECRET_KEY = "{get_random_string(length=50, allowed_chars=allowed_chars)}"\n""")
