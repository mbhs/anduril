from django.db import models


class Domain(models.Model):
    """Domains forwarded to this server for mail.

    Virtual domains are used when an address points to a server for
    web and other services but forwards mail to this server.
    """

    name = models.CharField(max_length=50)
    main = models.BooleanField(default=False)

    def __str__(self):
        """Represent the domain as a string."""

        return self.name

    def save(self, *args, **kwargs):
        """Save the domain and make sure there is only one default."""

        if self.main:
            for domain in Domain.objects.exclude(id=self.id).all():
                domain.main = False
        super().save(*args, **kwargs)

    @staticmethod
    def default():
        """Get default domain."""

        return Domain.objects.filter(main=True).first()


class Account(models.Model):
    """A mail account either for local hosting or forwarding.

    This is a generic mail account. It must have a unique email, and
    notice that the email redundantly contains the domain name due to
    Postfix limitations. This is checked in the save functionality.
    If the forward address is set, this account will be used as an
    alias. Otherwise, mail will be stored on the server.
    """

    domain = models.ForeignKey(Domain)
    address = models.EmailField(unique=True)
    forward = models.EmailField()

    def __str__(self):
        """Represent the account as a string."""

        return self.address

    def save(self, *args, **kwargs):
        """Save the account and check domain."""

        assert self.address.split("@")[1] == self.domain.name
        super().save(*args, **kwargs)
