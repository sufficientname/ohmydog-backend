from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

import datetime

from ohmydog.appointments import constants
from ohmydog.appointments import exceptions


class AppointmentManager(models.Manager):

    def create_appointment_request(self, user, pet, reason, date, timeslot):        
        days_to_booster = 0
        if reason == constants.REASON_VACCINATION_A:
            days_to_booster = check_vaccine_a(pet, date)

        elif reason == constants.REASON_VACCINATION_B:
            days_to_booster = check_vaccine_b(pet, date)

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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet = models.ForeignKey('pets.Pet', on_delete=models.CASCADE)
    reason = models.CharField(max_length=16, choices=constants.REASON_CHOICES)
    date = models.DateField()
    timeslot = models.CharField(max_length=16, choices=constants.TIMESLOT_CHOICES)
    hour = models.TimeField(null=True)
    suggestion_date = models.DateField(null=True)
    status = models.CharField(max_length=16, choices=constants.STATUS_CHOICES, default=constants.STATUS_PENDING)
    observations = models.TextField()
    days_to_booster = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=16 ,decimal_places=2, default=0)

    def booster_date(self):
        if not self.days_to_booster:
            return None
        return self.date + datetime.timedelta(days=self.days_to_booster)
    
    def can_accept(self):
        return (
            self.status == constants.STATUS_PENDING and
            self.date >= datetime.date.today()
        )

    def accept(self, hour, check=True):
        if check and not self.can_accept():
            return
        self.status = constants.STATUS_ACCEPTED
        self.hour = hour

    def can_reject(self):
        return (
            (self.status == constants.STATUS_PENDING) and
            (self.date >= datetime.date.today())
        )

    def reject(self, suggestion_date, check=True):
        if check and not self.can_reject():
            return
        self.status = constants.STATUS_REJECTED
        self.suggestion_date = suggestion_date

    def can_cancel(self):
        return (
            (self.status in [constants.STATUS_PENDING, constants.STATUS_ACCEPTED]) and
            (self.date >= datetime.date.today())
        )

    def cancel(self, check=True):
        if check and not self.can_cancel():
            return
        self.status = constants.STATUS_CANCELED

    def can_complete(self):
        return(
            (self.status == constants.STATUS_ACCEPTED) and
            (self.date <= datetime.date.today())
        )

    def complete(self, price, observations, check=True):
        if check and not self.can_complete():
            return
        self.status = constants.STATUS_COMPLETED
        self.price = price
        self.observations = observations

    def make_health_record_entries(self, weight):
        vaccine = self.get_vaccine()
        entries = []
        if weight:
            weight_entry = self.pet.make_weight_health_record_entry(self.date, weight, appointment=self)
            entries.append(weight_entry)
        if vaccine:
            vaccine_entry = self.pet.make_vaccine_health_record_entry(self.date, vaccine, appointment=self)
            entries.append(vaccine_entry)
        return entries

    def get_vaccine(self):
        if self.reason == constants.REASON_VACCINATION_A:
            return constants.VACCINE_A
        if self.reason == constants.REASON_VACCINATION_B:
            return constants.VACCINE_B
        return None
       

def get_last_appointment(pet, reason) -> Appointment:
    status = constants.STATUS_COMPLETED
    appointment = Appointment.objects.filter(
        pet=pet,
        reason=reason,
        status=status
    ).order_by('-date').first()
    return appointment
    

def check_vaccine_a(pet, date) -> int:
    pet_age = pet.age_at(date)

    # menores a 2 meses no pueden recibir vacuna A
    if pet_age.years == 0 and pet_age.months < 2:
        raise exceptions.BadReasonError("Mascotas menores a 2 meses no pueden recibir vacuna de tipo A.")

    last_appointment = get_last_appointment(pet, constants.REASON_VACCINATION_A)
    if last_appointment and last_appointment.booster_date() > date:
        raise exceptions.BadReasonError(f"Esta mascota ya recibio una vacuna de tipo A en los ultimos {last_appointment.days_to_booster} dias. Solicite un turno a partir del dia {last_appointment.booster_date()}.")

    # entre 2 y 4 meses necesitan refuerzo a los 21 dias
    if (pet_age.years == 0 and pet_age.months <= 4):
        return 21

    # mayores a 4 meses necesitan refuerzo a los 365 dias
    return 365


def check_vaccine_b(pet, date) -> int:
    pet_age = pet.age_at(date)

    # menores a 4 meses no pueden recibir vacuna tipo B
    if pet_age.years == 0 and pet_age.months < 4:
        raise exceptions.BadReasonError("Mascotas menores a 4 meses no pueden recibir vacuna de tipo B.")

    last_appointment = get_last_appointment(pet, constants.REASON_VACCINATION_B)
    if last_appointment and last_appointment.booster_date() > date:
        raise exceptions.BadReasonError(
            f"Esta mascota ya recibio una vacuna de tipo B en los ultimos {last_appointment.days_to_booster} dias. Solicite un turno a partir del dia {last_appointment.booster_date()}.")

    # mayores a 4 meses necesitan refuerzo a los 365 dias
    return 365