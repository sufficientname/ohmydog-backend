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