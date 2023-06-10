from django.db import models
from django.conf import settings

from ohmydog.adoptions import constants

class AdoptionAd(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    pet_name = models.CharField(max_length=32, null=True)
    pet_age = models.PositiveIntegerField(null=False)
    pet_gender = models.CharField(max_length=16, choices=constants.GENDER_CHOICES, null=False)
    pet_size = models.CharField(max_length=16, choices=constants.SIZE_CHOICES, null=False)
    status = models.CharField(max_length=16, choices=constants.STATUS_CHOICES, default=constants.STATUS_PUBLISHED, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)