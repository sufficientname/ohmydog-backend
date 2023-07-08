from django.db import models
from django.conf import settings

from ohmydog.advertisements import constants

class AbstractAd(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    status = models.CharField(max_length=16, choices=constants.STATUS_CHOICES, default=constants.STATUS_PUBLISHED, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        abstract = True

    def can_cancel(self):
        return self.status == constants.STATUS_PUBLISHED

    def cancel(self):
        if not self.can_cancel():
            return
        self.status = constants.STATUS_CANCELED

    def can_complete(self):
        return self.status == constants.STATUS_PUBLISHED

    def complete(self):
        if not self.can_complete():
            return
        self.status = constants.STATUS_COMPLETED

    def can_contact(self):
        return self.status == constants.STATUS_PUBLISHED