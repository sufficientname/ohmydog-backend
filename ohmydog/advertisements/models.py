from django.db import models
from django.conf import settings

import datetime

from ohmydog.advertisements import constants

class AbstractAd(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=constants.STATUS_CHOICES, default=constants.STATUS_PUBLISHED)
    created_at = models.DateTimeField(auto_now_add=True)
    pause_start_date = models.DateField(null=True)
    pause_end_date = models.DateField(null=True)

    class Meta:
        abstract = True

    def can_cancel(self):
        return self.status == constants.STATUS_PUBLISHED

    def cancel(self, check=True):
        if check and not self.can_cancel():
            return
        self.status = constants.STATUS_CANCELED

    def can_complete(self):
        return self.status == constants.STATUS_PUBLISHED

    def complete(self, check=True):
        if check and not self.can_complete():
            return
        self.status = constants.STATUS_COMPLETED
    
    def can_contact(self):
        return self.status == constants.STATUS_PUBLISHED

    def can_pause(self):
        return self.status == constants.STATUS_PUBLISHED
    
    def pause(self, check=True):
        if check and not self.can_pause():
            return
        self.status = constants.STATUS_PAUSED
        self.pause_start_date = None
        self.pause_end_date = None
        self.save()

    def pause_range(self, pause_start_date, pause_end_date, check=True):
        if check and not self.can_pause():
            return
        today = datetime.date.today()
        if pause_start_date <= today and pause_end_date >= today:
            self.status = constants.STATUS_PAUSED
        self.pause_start_date = pause_start_date
        self.pause_end_date = pause_end_date
        self.save()
    
    def can_unpause(self):
        return self.status == constants.STATUS_PAUSED

    def unpause(self):
        if not self.can_unpause():
            return
        self.status = constants.STATUS_PUBLISHED
        self.pause_start_date = None
        self.pause_end_date = None
        self.save()
    
    @classmethod
    def pause_inrange_ads(cls):
        today = datetime.date.today()
        updated = cls.objects.filter(
            status=constants.STATUS_PUBLISHED,
            pause_start_date__lte=today,
            pause_end_date__gte=today
        ).update(status=constants.STATUS_PAUSED)
        if updated:
            print(f'Updated {updated} ads to {constants.STATUS_PAUSED}')

    @classmethod
    def unpause_inrage_ads(cls):
        today = datetime.date.today()
        updated = cls.objects.filter(
            status=constants.STATUS_PAUSED,
            pause_end_date__lte=today
        ).update(
            status=constants.STATUS_PUBLISHED,
            pause_start_date=None,
            pause_end_date=None
        )
        if updated:
            print(f'Updated {updated} ads to {constants.STATUS_PUBLISHED}')
