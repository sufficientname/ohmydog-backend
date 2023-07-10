from django.db import models

import decimal
import datetime

from ohmydog.campaigns import constants


class Campaign(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    goal_amount = models.DecimalField(max_digits=16, decimal_places=2)
    current_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    status = models.CharField(max_length=16, choices=constants.STATUS_CHOICES, default=constants.STATUS_PUBLISHED)
    created_at = models.DateTimeField(auto_now_add=True)

    def add_current_amount(self, amount):
        self.current_amount += amount

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

    def can_donate(self):
        return self.status == constants.STATUS_PUBLISHED
    
    def make_donation(self, amount, donor_first_name, donor_last_name, donor_email, donor_phone_number, user=None):
        if user is not None and user.is_anonymous:
            user = None
        return CampaignDonation(
            campaign=self,
            user=user,
            amount=amount,
            donor_first_name=donor_first_name,
            donor_last_name=donor_last_name,
            donor_email=donor_email,
            donor_phone_number=donor_phone_number,
        )
    
    @classmethod
    def complete_ended_campaigns(cls):
        today = datetime.date.today()
        updated = cls.objects.filter(
            end_date__lt=today,
            status__in=[constants.STATUS_PUBLISHED]
        ).update(status=constants.STATUS_COMPLETED)
        if updated:
            print(f'Updated {updated} campaigns to {constants.STATUS_COMPLETED}')


class CampaignDonation(models.Model):
    campaign = models.ForeignKey('campaigns.Campaign', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    donor_first_name = models.CharField(max_length=150)
    donor_last_name = models.CharField(max_length=150)
    donor_email = models.EmailField()
    donor_phone_number = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_discount_amount(self):
        return self.amount * decimal.Decimal('0.2')