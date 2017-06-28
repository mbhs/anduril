from django import template

register = template.Library()


@register.filter(name="full_name")
def full_name(value):
    """Return the full name of a user."""

    return value.profile.full_name
