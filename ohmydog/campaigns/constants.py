from ohmydog.utils.choices import choice, make_choices
from django.utils.translation import gettext_lazy as _

STATUS_PUBLISHED = 'PUBLICADA'
STATUS_CANCELED = 'CANCELADA'
STATUS_COMPLETED = 'COMPLETADA'

STATUSES = {
    STATUS_PUBLISHED: choice(STATUS_PUBLISHED, _('Publicada')),
    STATUS_CANCELED: choice(STATUS_CANCELED, _('Cancelada')),
    STATUS_COMPLETED: choice(STATUS_COMPLETED, _('Completada')),
}

STATUS_CHOICES = make_choices(STATUSES)