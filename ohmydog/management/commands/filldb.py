from django.core.management.base import BaseCommand, CommandError

from ohmydog.users.models import User

from ohmydog.pets.models import Pet
from ohmydog.pets import constants as pets_constants

from ohmydog.appointments.models import Appointment
from ohmydog.appointments import constants as appointments_constants

from ohmydog.campaigns.models import Campaign
from ohmydog.campaigns import constants as campaigns_constants

import datetime 

class Command(BaseCommand):
    help = "Fills the db with some data"

    def handle(self, *args, **kwargs):
        admin = User.objects.create_superuser('admin', 'admin@mail.com', 'admin')
        self.stdout.write(self.style.SUCCESS('created admin: %s' % admin))

        user1 = User.objects.create_user(
            'user1@mail.com',
            'user1@mail.com',
            'user1',
            first_name='user',
            last_name='one',
            id_number='1111',
            phone_number='(221) 555-1111',
            birthdate=datetime.date(2001, 1, 1)
        )

        self.stdout.write(self.style.SUCCESS('created user: %s' % user1))
        
        user2 = User.objects.create_user(
            'user2@mail.com',
            'user2@mail.com',
            'user2',
            first_name='user',
            last_name='two',
            id_number='2222',
            phone_number='(221) 555-2222',
            birthdate=datetime.date(2002, 2, 2)
        )
        self.stdout.write(self.style.SUCCESS('created user: %s' % user2))

        user1pet1 = Pet.objects.create(
            user=user1, 
            name="user1_pet1",
            breed="caniche",
            gender=pets_constants.GENDER_MALE,
            color="negro",
            birthdate=datetime.date(2010, 1, 1)
        )
        self.stdout.write(self.style.SUCCESS('created pet: %s' % user1pet1))


        user1pet2 = Pet.objects.create(
            user=user1, 
            name="user1_pet2",
            breed="caniche",
            gender=pets_constants.GENDER_MALE,
            color="blanco",
            birthdate=datetime.date(2010, 2, 2)
        )
        self.stdout.write(self.style.SUCCESS('created pet: %s' % user1pet2))

        user2pet1 = Pet.objects.create(
            user=user2, 
            name="user2_pet1",
            breed="maltes",
            gender=pets_constants.GENDER_FEMALE,
            color="blanco",
            birthdate=datetime.date(2010, 2, 2)
        )
        self.stdout.write(self.style.SUCCESS('created pet: %s' % user2pet1))


        user3 = User.objects.create_user(
            'user3@mail.com',
            'user3@mail.com',
            'user3',
            first_name='user',
            last_name='three',
            id_number='3333',
            phone_number='(221) 555-3333',
            birthdate=datetime.date(2003, 3, 3)
        )

        under2months = Pet.objects.create(
            user=user3, 
            name="menor a 2 meses",
            breed="maltes",
            gender=pets_constants.GENDER_MALE,
            color="blanco",
            birthdate=datetime.date.today() - datetime.timedelta(days=45)
        )

        bewtween2and4months = Pet.objects.create(
            user=user3, 
            name="entre 2 y 4 meses",
            breed="maltes",
            gender=pets_constants.GENDER_FEMALE,
            color="blanco",
            birthdate=datetime.date.today() - datetime.timedelta(days=95)
        )

        over4months = Pet.objects.create(
            user=user3, 
            name="mayor a 4 meses",
            breed="maltes",
            gender=pets_constants.GENDER_MALE,
            color="blanco",
            birthdate=datetime.date.today() - datetime.timedelta(days=140)
        )

        bewtween2and4monthsWithVaccineA = Pet.objects.create(
            user=user3, 
            name="entre 2 y 4 meses con vacuna A",
            breed="maltes",
            gender=pets_constants.GENDER_FEMALE,
            color="blanco",
            birthdate=datetime.date.today() - datetime.timedelta(days=95)
        )

        vaccine_A_appointment = Appointment.objects.create_appointment_request(
            user3, 
            bewtween2and4monthsWithVaccineA,
            appointments_constants.REASON_VACCINATION_A,
            datetime.date.today() - datetime.timedelta(days=10),
            appointments_constants.TIMESLOT_AFTERNOON,
        )
        vaccine_A_appointment.accept("18:00", check=False)
        vaccine_A_appointment.complete(1000, "sin inconvenientes", check=False)
        vaccine_A_appointment.save()

        over4monthsWithVaccineAandB = Pet.objects.create(
            user=user3, 
            name="mayor a 4 meses con vacuna A y B",
            breed="maltes",
            gender=pets_constants.GENDER_MALE,
            color="blanco",
            birthdate=datetime.date.today() - datetime.timedelta(days=300)
        )

        vaccine_A_appointment = Appointment.objects.create_appointment_request(
            user3, 
            over4monthsWithVaccineAandB,
            appointments_constants.REASON_VACCINATION_A,
            datetime.date.today() - datetime.timedelta(days=10),
            appointments_constants.TIMESLOT_AFTERNOON,
        )
        vaccine_A_appointment.accept("18:00", check=False)
        vaccine_A_appointment.complete(1000, "sin inconvenientes", check=False)
        vaccine_A_appointment.save()

        vaccine_B_appointment = Appointment.objects.create_appointment_request(
            user3, 
            over4monthsWithVaccineAandB,
            appointments_constants.REASON_VACCINATION_B,
            datetime.date.today() - datetime.timedelta(days=10),
            appointments_constants.TIMESLOT_AFTERNOON,
        )
        vaccine_B_appointment.accept("18:00", check=False)
        vaccine_B_appointment.complete(1000, "sin inconvenientes", check=False)
        vaccine_B_appointment.save()


        Appointment.objects.create_appointment_request(
            user3, 
            over4monthsWithVaccineAandB,
            appointments_constants.REASON_CONSULTATION,
            datetime.date.today() - datetime.timedelta(days=30),
            appointments_constants.TIMESLOT_AFTERNOON,
        )

        Campaign.objects.create(
            name="Refugios caninos de La Plata",
            description="En esta campaña recaudaremos fondos para los refugios caninos de la ciudad de La Plata",
            end_date=datetime.date(year=2200, month=12, day=31),
            status=appointments_constants.STATUS_PUBLISHED,
        )