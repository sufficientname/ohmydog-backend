from django.db import models

from ohmydog.advertisements.models import AbstractAd
from ohmydog.advertisements.petsitters import constants


class PetSitterAd(AbstractAd):
    sitter_first_name = models.CharField(max_length=150)
    sitter_last_name = models.CharField(max_length=150)
    sitter_email = models.EmailField()
    sitter_phone_number = models.CharField(max_length=32)
    service_type = models.CharField(max_length=16, choices=constants.SERVICE_TYPE_CHOICES)
    service_area = models.CharField(max_length=128)
