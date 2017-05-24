"""Isolates functions that use customizable formats or methods.

This module is primarily for generating usernames, which have several
templates based on availability.
"""

import itertools
import string


def filter_name(name):
    """Remove all special characters and lowercase."""

    return "".join(filter(lambda c: c in string.ascii_lowercase, name.lower()))


def generate_username(first_name, last_name):
    """Create a username generator from a person's information."""

    # Sean H Gabaree
    first = filter_name(first_name)
    last = filter_name(last_name)

    # segabare
    yield first[:2] + last[:6]

    # segabaree
    for i in range(1, len(last) - 6 + 1):
        yield first[:2] + last[:6+i]

    # seagabar
    for i in range(1, len(first) - 2 + 1):
        yield first[:2+i] + last

    # segabaree
    for i in range(1, len(last) - 6 + 1):
        yield first + last[:6+i]

    # segabaree0
    for i in itertools.count():
        yield first[:2] + last + str(i)
