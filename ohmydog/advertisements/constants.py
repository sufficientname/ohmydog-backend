from ohmydog.utils.choices import choice, make_choices
from django.utils.translation import gettext_lazy as _


STATUS_PUBLISHED =  'PUB'
STATUS_COMPLETED = 'COM'
STATUS_CANCELED = 'CAN'

STATUSES = {
    STATUS_PUBLISHED: choice(STATUS_PUBLISHED, _('Publicado')),
    STATUS_COMPLETED: choice(STATUS_COMPLETED, _('Completado')),
    STATUS_CANCELED: choice(STATUS_CANCELED, _('Cancelado')),
}

STATUS_CHOICES = make_choices(STATUSES)