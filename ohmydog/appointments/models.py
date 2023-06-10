from django.db import models
from django.conf import settings

import datetime

from ohmydog.appointments import constants
from ohmydog.appointments import exceptions


class AppointmentManager(models.Manager):

    def create_appointment_request(self, user, pet, reason, date, timeslot):        
        days_to_booster = 0
        if reason == constants.REASON_VACCINATION_A:
            days_to_booster = check_vaccine_a(pet)

        elif reason == constants.REASON_VACCINATION_B:
            days_to_booster = check_vaccine_b(pet)

        appointment = self.model(
            user=user,
            pet=pet,
            reason=reason,
            date=date,
            timeslot=timeslot,
            days_to_booster = days_to_booster
        )
        appointment.save()

        return appointment

class Appointment(models.Model):
    objects = AppointmentManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    pet = models.ForeignKey('pets.Pet', on_delete=models.CASCADE, null=False)
    reason = models.CharField(max_length=16, choices=constants.REASON_CHOICES, null=False)
    date = models.DateField(null=False)
    timeslot = models.CharField(max_length=16, choices=constants.TIMESLOT_CHOICES, null=False)
    hour = models.TimeField(null=True)
    suggestion_date = models.DateField(null=True)
    status = models.CharField(max_length=16, choices=constants.STATUS_CHOICES, default=constants.STATUS_PENDING, null=False)
    observations = models.TextField(null=False)
    days_to_booster = models.PositiveIntegerField(null=False)
    price = models.PositiveIntegerField(null=False, default=0)

    def booster_date(self):
        if not self.days_to_booster:
            return None
        return self.date + datetime.timedelta(days=self.days_to_booster)
    
    def can_accept(self):
        return (
            self.status == constants.STATUS_PENDING and
            self.date > datetime.date.today()
        )

    def accept(self, hour):
        if not self.can_accept():
            return
        self.status = constants.STATUS_ACCEPTED
        self.hour = hour

    def can_reject(self):
        return (
            (self.status == constants.STATUS_PENDING) and
            (self.date > datetime.date.today())
        )

    def reject(self, suggestion_date):
        if not self.can_reject():
            return
        self.status = constants.STATUS_REJECTED
        self.suggestion_date = suggestion_date

    def can_cancel(self):
        return (
            (self.status in [constants.STATUS_PENDING, constants.STATUS_ACCEPTED]) and
            (self.date > datetime.date.today())
        )

    def cancel(self):
        if not self.can_cancel():
            return
        self.status = constants.STATUS_CANCELED

    def can_complete(self):
        return(
            (self.status == constants.STATUS_ACCEPTED) and
            (self.date <= datetime.date.today())
        )

    def complete(self, price, observations):
        if not self.can_complete():
            return
        self.status = constants.STATUS_COMPLETED
        self.price = price
        self.observations = observations


    

def check_vaccine_a(pet) -> int:
    pet_months = pet.age_months()

    # menores a 2 meses no pueden recibir vacuna A
    if pet_months < 2:
        raise exceptions.BadReasonError("mascotas menores a 2 meses no pueden recibir vacuna de tipo A")

    # entre 2 y 4 meses necesitan refuerzo a los 21 dias
    if pet_months <= 4:
        return 21

    # mayores a 4 meses necesitan refuerzo a los 365 dias
    return 365
    
def check_vaccine_b(pet):
    pet_months = pet.age_months()

    # menores a 4 meses no pueden recibir vacuna tipo B
    if pet_months < 4:
        raise exceptions.BadReasonError("mascotas menores a 4 meses no pueden recibir vacuna de tipo B")

    # mayores a 4 meses necesitan refuerzo a los 365 dias
    return 365