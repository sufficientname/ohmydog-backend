import datetime

import phonenumbers
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class PhoneNumberField(serializers.CharField):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(validate_phonenumber)


def validate_phonenumber(value):
    try:
        number = phonenumbers.parse(value, region='AR')
        if not phonenumbers.is_valid_number(number):
            raise serializers.ValidationError(_('Introduzca un número de teléfono válido.'))
    except phonenumbers.NumberParseException:
        raise serializers.ValidationError(_('Introduzca un número de teléfono válido.'))
    return value


class CreditCardSerializer(serializers.Serializer):
    name_on_card = serializers.CharField(max_length=300)
    card_number = serializers.CharField(max_length=16)
    cvv = serializers.CharField(max_length=3)
    expiration_date = serializers.DateField()

    def validate_card_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(_('El número de tarjeta debe ser numérico'))
        if len(value) != 16:
            raise serializers.ValidationError(_('El número de tarjeta debe tener 16 dígitos'))
        return value

    def validate(self, attrs):
        # invalid card
        FAKE_INVALID_CARD_NUMBER = '9999999999999999'
        FAKE_INVALID_CARD_CVV = '999'
        if (attrs['card_number'] == FAKE_INVALID_CARD_NUMBER and attrs['cvv'] == FAKE_INVALID_CARD_CVV):
            raise serializers.ValidationError(_('La tarjeta es invalida'))
        
        # insufficient funds
        FAKE_INSUFFICIENT_FUNDS_CARD_NUMBER = '8888888888888888'
        FAKE_INSUFFICIENT_FUNDS_CARD_CVV = '888'
        if (attrs['card_number'] == FAKE_INSUFFICIENT_FUNDS_CARD_NUMBER) and (attrs['cvv'] == FAKE_INSUFFICIENT_FUNDS_CARD_CVV):
            raise serializers.ValidationError(_('La tarjeta no cuenta con fondos suficientes'))
        
        # expired card
        if (attrs['expiration_date'] < datetime.date.today()):
            raise serializers.ValidationError(_('La tarjeta esta vencida'))

        return attrs