from django.db import models

from ohmydog.advertisements.models import AbstractAd
from ohmydog.advertisements.adoptions import constants


class AdoptionAd(AbstractAd):
    pet_name = models.CharField(max_length=32)
    pet_age = models.PositiveIntegerField()
    pet_gender = models.CharField(max_length=16, choices=constants.GENDER_CHOICES)
    pet_size = models.CharField(max_length=16, choices=constants.SIZE_CHOICES)
