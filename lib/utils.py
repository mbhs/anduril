"""Utilities referenced in views models."""

from django.http import Http404


def profile_type(*types):
    """Require specific profile types to access a view."""

    def decorator(view):
        """Wraps the underlying view function."""

        def view_wrapper(request, *args, **kwargs):
            """View that requires profile type to be in specified."""

            if request.user and request.user.profile and request.user.profile.type in types:
                return view(request, *args, **kwargs)
            else:
                raise Http404()

        return view_wrapper

    return decorator
