from django.core.management.base import BaseCommand, CommandError

from ohmydog.users.models import User
from ohmydog.pets.models import Pet

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
            phone_number='(221) 111-1111',
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
            phone_number='(221) 222-2222',
            birthdate=datetime.date(2002, 2, 2)
        )
        self.stdout.write(self.style.SUCCESS('created user: %s' % user2))

        user1pet1 = Pet.objects.create(
            user=user1, 
            name="user1_pet1",
            breed="caniche",
            color="negro",
            birthdate=datetime.date(2010, 1, 1)
        )
        self.stdout.write(self.style.SUCCESS('created pet: %s' % user1pet1))


        user1pet2 = Pet.objects.create(
            user=user1, 
            name="user1_pet2",
            breed="caniche",
            color="blanco",
            birthdate=datetime.date(2010, 2, 2)
        )
        self.stdout.write(self.style.SUCCESS('created pet: %s' % user1pet2))

        user2pet1 = Pet.objects.create(
            user=user2, 
            name="user2_pet1",
            breed="maltes",
            color="blanco",
            birthdate=datetime.date(2010, 2, 2)
        )
        self.stdout.write(self.style.SUCCESS('created pet: %s' % user2pet1))
