from django import template

import subprocess
import re


register = template.Library()
cache = {}


def clean(string):
    """Filter escape codes."""

    return re.sub(r"(\x9B|\x1B\[)[0-?]*[ -\\/]*[@-~]|\x1B[=>]", "", string.strip()).strip()


def cached(func):
    """Cache the result of a shell call.

    This may be cached because the server is restarted whenever it
    actually changes.
    """

    def wrapper(*args, **kwargs):
        if func not in cache:
            cache[func] = func(*args, **kwargs)
        return cache[func]

    return wrapper


@register.simple_tag(name="commit_hash")
@cached
def commit_hash():
    """Get the most recent commit hash."""

    with subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE) as process:
        return clean(process.stdout.read().decode())


@register.simple_tag(name="commit_hash_short")
@cached
def commit_hash_short():
    """Get the most recent commit hash."""

    with subprocess.Popen(["git", "rev-parse", "--short", "HEAD"], stdout=subprocess.PIPE) as process:
        return clean(process.stdout.read().decode())


@register.simple_tag(name="commit_date")
@cached
def commit_date():
    """Get the most recent commit date."""

    with subprocess.Popen(["git", "log", "--no-decorate", "-l", "--format=%cd"], stdout=subprocess.PIPE) as process:
        return clean(process.stdout.read().decode())


@register.simple_tag(name="commit_author")
@cached
def commit_author():
    """Get the most recent commit author."""

    with subprocess.Popen(["git", "log", "--no-decorate", "-1", "--format=%an"], stdout=subprocess.PIPE) as process:
        return clean(process.stdout.read().decode())
