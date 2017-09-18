from oidc_provider.lib.claims import ScopeClaims


class CustomScopeClaims(ScopeClaims):
    """The scope claims for Anduril."""

    def scope_profile(self):
        """Populate the scope claim dictionary."""

        return {
            "id": self.user.id,
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
        }

    def scope_email(self):
        """Get email information for a user."""

        return {
            "email": self.user.email,
        }
