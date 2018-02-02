"""Customized settings for Anduril production deployment."""

import yaml

from . import *


# Grab details from the configuration file in the root directory
try:
    with open(os.path.join(BASE_DIR, "production.yaml")) as file:
        config = yaml.load(file)
except FileNotFoundError:
    print("Could not find a production.yaml file in the root directory!")
    import sys
    sys.exit(1)


# Set new URLs for the site
ALLOWED_HOSTS = ["home.mbhs.edu", "localhost"]
SITE_URL = "https://home.mbhs.edu"


# Use the production database
database = config["database"]
DATABASES = {
    "default": {
        "ENGINE": database["engine"],
        "NAME": database["name"],
        "USER": database.get("user", ""),
        "PASSWORD": database.get("password", ""),
        "HOST": database.get("host", "localhost"),
        "PORT": database.get("port", ""),
    }
}


# Logging configuration
# https://docs.djangoproject.com/en/1.11/topics/logging/

LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_PATH = os.path.join(LOG_DIR, "anduril.log")

if not os.path.isdir(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": os.path.join("logs", "anduril.log"),
        }
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": False
        }
    }
}
