"""Customized settings for Anduril production deployment."""

import yaml

from . import *


with open(os.path.join(BASE_DIR, "production.yaml")) as file:
    config = yaml.load(file)

SECRET_KEY = config["secret"]

ALLOWED_HOSTS = ["home.mbhs.edu", "localhost"]

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config["database"]["name"],
        "USER": config["database"]["user"],
        "PASSWORD": config["database"]["password"],
        "HOST": "localhost",
        "PORT": "",
    }
}
