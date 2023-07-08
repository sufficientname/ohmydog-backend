from ohmydog.utils.choices import choice, make_choices
from django.utils.translation import gettext_lazy as _


SERVICE_TYPE_SITTER = 'CUIDADOR'
SERVICE_TYPE_WALKER = 'PASEADOR'

SERVICE_TYPES = {
    SERVICE_TYPE_SITTER: choice(SERVICE_TYPE_SITTER, _('Cuidador')),
    SERVICE_TYPE_WALKER: choice(SERVICE_TYPE_WALKER, _('Paseador')),
}

SERVICE_TYPE_CHOICES = make_choices(SERVICE_TYPES)