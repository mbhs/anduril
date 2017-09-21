from oidc_provider.lib.claims import ScopeClaims

from core.models import UserProfile


class CustomScopeClaims(ScopeClaims):
    """The scope claims for Anduril."""

    info_profile = ("Profile information", "Username, name, and student or staff identification.")

    def scope_profile(self):
        """Populate the scope claim dictionary."""

        base = {
            "id": self.user.id,
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "type": self.user.profile.type}
        if self.user.profile.type == UserProfile.STUDENT:
            base["student_id"] = self.user.profile.student_id
        return base

    info_email = ("Email address", "Email address and verification.")

    def scope_email(self):
        """Get email information for a user."""

        return {"email": self.user.email}
