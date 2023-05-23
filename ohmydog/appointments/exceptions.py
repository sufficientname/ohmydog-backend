class AppointmentError(Exception):
    pass

class BadReasonError(AppointmentError):
    pass