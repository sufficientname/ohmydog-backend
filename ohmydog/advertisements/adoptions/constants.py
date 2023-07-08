from ohmydog.utils.choices import choice, make_choices
from django.utils.translation import gettext_lazy as _


GENDER_MALE = 'MACHO'
GENDER_FEMALE = 'HEMBRA'

GENDERS = {
    GENDER_MALE: choice(GENDER_MALE, _('Macho')),
    GENDER_FEMALE: choice(GENDER_FEMALE, _('Hembra')),
}

GENDER_CHOICES = make_choices(GENDERS)


SIZE_SMALL = 'PEQUENO'
SIZE_MEDIUM = 'MEDIANO'
SIZE_BIG = 'GRANDE'

SIZES = {
    SIZE_SMALL: choice(SIZE_SMALL, _('Pequeño')),
    SIZE_MEDIUM: choice(SIZE_MEDIUM, _('Mediano')),
    SIZE_BIG: choice(SIZE_BIG, _('Grande')),
}

SIZE_CHOICES = make_choices(SIZES)
