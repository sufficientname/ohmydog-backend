from ohmydog.utils.choices import choice, make_choices
from django.utils.translation import gettext_lazy as _


ENTRY_TYPE_VACCINE = 'VACUNA'
ENTRY_TYPE_WEIGHT = 'PESO'

ENTRY_TYPES = {
    ENTRY_TYPE_VACCINE: choice(ENTRY_TYPE_VACCINE, _('Vacuna')),
    ENTRY_TYPE_WEIGHT: choice(ENTRY_TYPE_WEIGHT, _('Peso')),
}

ENTRY_TYPE_CHOICES = make_choices(ENTRY_TYPES)


VACCINE_A = "VACUNA_A"
VACCINE_B = "VACUNA_B"

VACCINES = {
    VACCINE_A: choice(VACCINE_A, _('Vacuna A')),
    VACCINE_B: choice(VACCINE_B, _('Vacuna B')),
}

VACCINE_CHOICES = make_choices(VACCINES)
