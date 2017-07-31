from django.views.generic import View
from django.shortcuts import HttpResponse


class ProfileBasedViewDispatcher(View):
    """Returns responses based on the request user type."""

    lookup = {}
    default = HttpResponse(status=404)

    def dispatch(self, request, *args, **kwargs):
        """Return the response according to the lookup."""

        if not request.user.profile:
            print("User does not have an attached profile!")
            return HttpResponse(status=500)

        return self.lookup.get(request.user.profile.type, self.default)(request, *args, **kwargs)
