import random

ALLOWED_CHARACTERS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_LENGTH = 50


def generate(characters=ALLOWED_CHARACTERS, length=SECRET_LENGTH):
    """Generate the secret."""

    return "".join(random.SystemRandom().choice(characters) for _ in range(length))


def get(path):
    """Get the secret from a secret file."""

    try:
        with open(path) as file:
            return file.read().strip()  # Strip may not be necessary
    except (FileNotFoundError, OSError):
        secret = generate()
        with open(path, "w") as file:
            file.write(secret)
