from django.db import models
from django.conf import settings

import datetime
from dateutil import relativedelta

from ohmydog.pets import constants


class Pet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    breed = models.CharField(max_length=32)
    color = models.CharField(max_length=32)
    gender = models.CharField(max_length=16, choices=constants.GENDER_CHOICES)
    birthdate = models.DateField()

    class Meta:
        unique_together = [['name', 'user']]

    def __str__(self):
        return f'{self.name} ({self.age_months()})'

    def age_at(self, date):
        return relativedelta.relativedelta(date, self.birthdate)

    def age(self):
        return self.age_at(datetime.date.today())

    def _age(self):
        return datetime.date.today() - self.birthdate

    def age_days(self):
        return self._age().days

    def age_months(self):
        days = self.age_days()
        return int((days/365)*12)

    def age_years(self):
        days = self.age_days()
        return int(days/365)
    
    def _make_health_record_entry(self, date, entry_type, vaccine=None, weight=None, appointment=None):
        return HealthRecordEntry(
            pet=self,
            date=date,
            entry_type=entry_type,
            vaccine=vaccine,
            weight=weight,
            appointment=appointment,
        )
    
    def make_vaccine_health_record_entry(self, date, vaccine, appointment=None):
        return self._make_health_record_entry(date, constants.ENTRY_TYPE_VACCINE, vaccine=vaccine, appointment=appointment)

    def make_weight_health_record_entry(self, date, weight, appointment=None):
        return self._make_health_record_entry(date, constants.ENTRY_TYPE_WEIGHT, weight=weight, appointment=appointment)


class HealthRecordEntry(models.Model):
    pet = models.ForeignKey('pets.Pet', on_delete=models.CASCADE)
    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    entry_type = models.CharField(max_length=16, choices=constants.ENTRY_TYPE_CHOICES)
    vaccine = models.CharField(max_length=16, null=True)
    weight = models.DecimalField(max_digits=16, decimal_places=2, null=True)

    @property
    def entry_value(self):
        if self.entry_type == constants.ENTRY_TYPE_VACCINE:
            return self.vaccine
        if self.entry_type == constants.ENTRY_TYPE_WEIGHT:
            return self.weight
        return None