from django.db import models
from django.conf import settings

import datetime


class Pet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=32, null=False, blank=False)
    breed = models.CharField(max_length=32, null=False, blank=False)
    color = models.CharField(max_length=32, null=False, blank=False)
    birthdate = models.DateField(null=False)

    class Meta:
        unique_together = [["name", "user"]]

    def __str__(self):
        return f'{self.name} ({self.age_months()})'

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

