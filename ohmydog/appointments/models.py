from django.db import models
from django.conf import settings

import datetime

from ohmydog.appointments import constants
from ohmydog.appointments import exceptions


class AppointmentManager(models.Manager):

    def create_appointment_request(self, user, pet, reason, request_date, request_timeslot):        
        days_to_booster = 0
        if reason == constants.REASON_VACCINATION_A:
            days_to_booster = check_vaccine_a(pet)

        elif reason == constants.REASON_VACCINATION_B:
            days_to_booster = check_vaccine_b(pet)

        appointment = self.model(
            user=user,
            pet=pet,
            reason=reason,
            request_date=request_date,
            request_timeslot=request_timeslot,
            days_to_booster = days_to_booster
        )
        appointment.save()

        return appointment

class Appointment(models.Model):
    objects = AppointmentManager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.Model, null=False)
    pet = models.ForeignKey('pets.Pet', on_delete=models.CASCADE, null=False)
    reason = models.CharField(max_length=16, choices=constants.REASON_CHOICES, null=False)
    request_date = models.DateField(null=False)
    request_timeslot = models.CharField(max_length=16, choices=constants.TIMESLOT_CHOICES, null=False)
    actual_datetime = models.DateTimeField(null=True)
    suggestion_datetime = models.DateTimeField(null=True)
    status = models.CharField(max_length=16, choices=constants.STATUS_CHOICES, default=constants.STATUS_PENDING, null=False)
    observations = models.TextField(null=False)
    days_to_booster = models.IntegerField(null=False)

    def approve(self, actual_datetime: datetime.datetime):
        if self.status != constants.STATUS_PENDING:
            return
        self.status = constants.STATUS_APPROVED
        self.actual_datetime = actual_datetime

    def reject(self, suggestion_datetime: datetime.datetime):
        if self.status != constants.STATUS_PENDING:
            return
        self.status = constants.STATUS_REJECTED
        self.suggestion_datetime = suggestion_datetime

    def cancel(self):
        if self.status not in [constants.STATUS_PENDING, constants.STATUS_APPROVED]:
            return
        self.status = constants.STATUS_CANCELED


    

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