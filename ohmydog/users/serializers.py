from rest_framework import serializers

from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

import datetime
from dateutil import relativedelta

from ohmydog.users.models import User
from ohmydog.users import constants
from ohmydog.serializers import PhoneNumberField


class UserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'id_number',
            'phone_number',
            'birthdate',
            'password_set',
            'discount_amount',
        ]
        read_only_fields = [
            'id',
            'is_staff',
            'discount_amount',
        ]

    def validate_birthdate(self, value):
        today = datetime.date.today()
        age = relativedelta.relativedelta(today, value)
        if age.years < constants.MIN_USER_AGE:
            raise serializers.ValidationError(_('Solo se permiten usuarios de 18 o mas años de edad.'))
        return value

    def create(self, validated_data):
        password = make_random_password()

        user = self.Meta.model.objects.create_user(
            validated_data['email'],
            email=validated_data['email'],
            password=password,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            id_number=validated_data['id_number'],
            phone_number=validated_data['phone_number'],
            birthdate=validated_data['birthdate'],
        )

        send_mail(
            _('Bienvenido a Oh my dog!'),
            _('Su contraseña es %(password)s.')
                % dict(
                    password=password
                ),
            settings.EMAIL_DEFAULT_FROM,
            [user.email],
            fail_silently=True,
        )

        return user


class UserPasswordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'password',
        ]

    def to_representation(self, instance):
        return UserSerializer(instance, context=self.context).to_representation(instance)

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.password_set = True
        instance.save()
        request = self.context.get('request', None)
        if request is not None:
            update_session_auth_hash(request, request.user)
        return instance


def make_random_password():
    return "12345"

