from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    id_number = models.CharField(_("dni"), max_length=32, unique=True)
    phone_number = models.CharField(_("phone number"), max_length=32)
    birthdate = models.DateField(_("birth date"), null=True)
    password_set = models.BooleanField(_("password set"), default=False)
    discount_amount = models.DecimalField(_("discount amount"), max_digits=16, decimal_places=2, default=0)

    def add_discount_amount(self, amount):
        self.discount_amount += amount
    
    def reset_discount_amount(self):
        self.discount_amount = 0