from ohmydog.utils.choices import choice, make_choices


GENDER_MALE = 'MALE'
GENDER_FEMALE = 'FEMALE'

GENDERS = {
    GENDER_MALE: choice(GENDER_MALE, 'Macho'),
    GENDER_FEMALE: choice(GENDER_FEMALE, 'Hembra'),
}

GENDER_CHOICES = make_choices(GENDERS)


SIZE_SMALL = 'SMALL'
SIZE_MEDIUM = 'MEDIUM'
SIZE_BIG = 'BIG'

SIZES = {
    SIZE_SMALL: choice(SIZE_SMALL, 'Pequeño'),
    SIZE_MEDIUM: choice(SIZE_MEDIUM, 'Mediano'),
    SIZE_BIG: choice(SIZE_BIG, 'Grande'),
}

SIZE_CHOICES = make_choices(SIZES)


STATUS_PUBLISHED =  'PUB'
STATUS_COMPLETED = 'COM'
STATUS_CANCELED = 'CAN'

STATUSES = {
    STATUS_PUBLISHED: choice(STATUS_PUBLISHED, 'Publicado'),
    STATUS_COMPLETED: choice(STATUS_COMPLETED, 'Completado'),
    STATUS_CANCELED: choice(STATUS_CANCELED, 'Cancelado')
}

STATUS_CHOICES = make_choices(STATUSES)