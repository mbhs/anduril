from oidc_provider.lib.claims import ScopeClaims

from core.models import UserProfile


class CustomScopeClaims(ScopeClaims):
    """The scope claims for Anduril."""

    info_profile = ("Profile information", "Username, name, and student or staff identification.")

    def scope_profile(self):
        """Populate the scope claim dictionary."""

        return {
            "id": self.user.id,
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "type": self.user.profile.type}

    info_id = ("Student ID", "Student ID number, if applicable.")

    def scope_id(self):
        """Get student ID."""

        if self.user.profile.type == UserProfile.STUDENT:
            return {"student_id": self.user.profile.student_id}

    info_email = ("Email address", "Email address and verification.")

    def scope_email(self):
        """Get email information for a user."""

        return {"email": self.user.email}
