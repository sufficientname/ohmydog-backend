from django_filters import rest_framework as filters
from ohmydog.appointments.models import Appointment

class AppointmentFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = Appointment
        fields = ['pet', 'status', 'date']