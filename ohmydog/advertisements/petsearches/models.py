from django.db import models

from ohmydog.advertisements.models import AbstractAd
from ohmydog.advertisements.petsearches import constants


class PetSearchAd(AbstractAd):
    pet_name = models.CharField(max_length=32)
    pet_age = models.PositiveIntegerField()
    pet_gender = models.CharField(max_length=16, choices=constants.GENDER_CHOICES)
    pet_breed = models.CharField(max_length=32)
    pet_size = models.CharField(max_length=16, choices=constants.SIZE_CHOICES)
    pet_color = models.CharField(max_length=32)
    last_seen_area = models.CharField(max_length=512)