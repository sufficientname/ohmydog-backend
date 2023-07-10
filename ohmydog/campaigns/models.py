from django.db import models

from ohmydog.campaigns import constants


class Campaign(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    goal_amount = models.DecimalField(max_digits=16, decimal_places=2)
    status = models.CharField(max_length=16, choices=constants.STATUS_CHOICES, default=constants.STATUS_PUBLISHED)

    def current_amount(self):
        return self.campaigndonation_set.aggregate(models.Sum('amount'))

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
    
    def make_donation(self, amount, donor_first_name, donor_last_name, donor_email, donor_phone_number):
        return CampaignDonation(
            campaign=self,
            amount=amount,
            donor_first_name=donor_first_name,
            donor_last_name=donor_last_name,
            donor_email=donor_email,
            donor_phone_number=donor_phone_number,
        )


class CampaignDonation(models.Model):
    campaign = models.ForeignKey('campaigns.Campaign', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    donor_first_name = models.CharField(max_length=150)
    donor_last_name = models.CharField(max_length=150)
    donor_email = models.EmailField()
    donor_phone_number = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)