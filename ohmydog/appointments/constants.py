TIMESLOT_CHOICES = [
    ('MANANA', 'Mañana'),
    ('TARDE', 'Tarde'),
]

REASON_CONSULTATION = "CONSULTA_GENERAL"
REASON_VACCINATION_A = "VACUNACION_A"
REASON_VACCINATION_B = "VACUNACION_B"
REASON_DEWORMING = "DESPARASITACION"
REASON_CASTRATION = "CASTRACION"
REASON_URGENCY = "URGENCIA"


REASON_CHOICES = [
    (REASON_CONSULTATION, 'Consulta general'),
    (REASON_VACCINATION_A, 'Vacunacion A'),
    (REASON_VACCINATION_B, 'Vacunacion B'),
    (REASON_DEWORMING, 'Desparasitacion'),
    (REASON_CASTRATION, 'Castracion'),
    (REASON_URGENCY, 'Urgencia'),
]

STATUS_PENDING = 'PEN'
STATUS_APPROVED = 'APR'
STATUS_REJECTED = 'REJ'
STATUS_CANCELED = 'CAN'
STATUS_COMPLETED = 'COM'

STATUS_CHOICES = [
    (STATUS_PENDING, 'Pending'),
    (STATUS_APPROVED, 'Approved'),
    (STATUS_REJECTED, 'Rejected'),
    (STATUS_CANCELED, 'Canceled'),
    (STATUS_COMPLETED, 'Completed'),
]