"""Utilities referenced in views models."""

from django.http import Http404


def profile_type(*types):
    """Require specific profile types to access a view."""

    def decorator(view):
        """Wraps a view function."""

        def view_wrapper(request, *args, **kwargs):
            """Represents the actual view function."""

            if request.user and request.user.profile and request.user.profile.type in types:
                return view(request, *args, **kwargs)
            else:
                raise Http404()

        return view_wrapper

    return decorator
