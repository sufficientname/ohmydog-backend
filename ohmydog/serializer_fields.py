import phonenumbers
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class PhoneNumberField(serializers.CharField):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validators.append(validate_phonenumber)


def validate_phonenumber(value):
    number = value
    if not number.startswith("+54"):
        number = f"+54 {number}"
    try:
        phonenumbers.parse(number)
    except phonenumbers.NumberParseException:
        raise serializers.ValidationError(_('Introduzca un número de teléfono válido.'))
    return value