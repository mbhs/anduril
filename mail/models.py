from django.db import models

from core.models import User

import os


class Domain(models.Model):
    """Domains forwarded to this server for mail.

    Virtual domains are used when an address points to a server for
    web and other services but forwards mail to this server.
    """

    name = models.CharField(max_length=50)
    default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Save the domain and make sure there is only one default."""

        if self.default:
            for domain in Domain.objects.exclude(self).all():
                domain.default = False
        super().save(*args, **kwargs)

    @staticmethod
    def default():
        """Get default domain."""


class Mailbox(models.Model):
    """A locally hosted mailbox account.

    The mailbox is handled by postfix. Given a domain and account
    name, this model stores where the mail directory should be
    located on the server.
    """

    domain = models.ForeignKey(Domain)
    name = models.CharField(max_length=50)
    directory = models.CharField(max_length=102)

    def __init__(self, domain, name):
        """Initialize a new mailbox with a default directory."""

        super().__init__(domain=domain, name=name)
        self.directory = os.path.join(domain.name, name)


class Alias(models.Model):
    """A mail alias that forwards to an external email."""

    domain = models.ForeignKey(Domain)
    name = models.CharField(max_length=100)
    forward = models.EmailField()


class Account(models.Model):
    """Create a mail account linked to a user."""

    user = models.ForeignKey(User)
    mailbox = models.ForeignKey(Mailbox, null=True)
    alias = models.ForeignKey(Alias, null=True)

    def save(self, *args, **kwargs):
        """Save the user mail mapping."""

        if self.mailbox is not None and self.alias is not None:
            raise RuntimeError("Cannot have both a mailbox and alias.")

    @staticmethod
    def setup(user, domain=None):
        """Create a new mail account for a user. Default to mailbox."""

        self = Account()
        self.user = user
        self.mailbox = Mailbox(domain=domain or Domain.default(), name=user.username)
