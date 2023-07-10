from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from ohmydog import permissions
from ohmydog.appointments.models import Appointment
from ohmydog.appointments.filters import AppointmentFilter
from ohmydog.appointments.serializers import (
    AppointmentSerializer,
    AppointmentRequestSerializer,
    AppointmentAcceptSerializer,
    AppointmentRejectSerializer,
    AppointmentCancelSerializer,
    AppointmentCompleteSerializer
)


class AppointmentViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    permission_classes = [permissions.IsCustomerUser]
    filterset_fields = ['pet', 'status']

    def get_queryset(self):
        Appointment.cancel_pending_and_accepted_appointments()
        user = self.request.user
        return Appointment.objects.filter(user=user).order_by('date', 'hour')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AppointmentRequestSerializer
        if self.action == 'cancel':
            return AppointmentCancelSerializer
        return AppointmentSerializer

    @action(methods=['POST'], detail=True, url_path='cancel')
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        serializer = self.get_serializer(appointment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AppointmentAdminViewSet(mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    permission_classes = [permissions.IsAdminUser]
    # filterset_fields = ['pet', 'status', 'date']
    filterset_class = AppointmentFilter

    def get_queryset(self):
        Appointment.cancel_pending_and_accepted_appointments()
        return Appointment.objects.all().order_by('date', 'hour')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AppointmentRequestSerializer
        if self.action == 'accept':
            return AppointmentAcceptSerializer
        if self.action == 'reject':
            return AppointmentRejectSerializer
        if self.action == 'complete':
            return AppointmentCompleteSerializer
        return AppointmentSerializer

    @action(methods=['POST'], detail=True, url_path='accept')
    def accept(self, request, pk=None):
        appointment = self.get_object()
        serializer = self.get_serializer(appointment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['POST'], detail=True, url_path='reject')
    def reject(self, request, pk=None):
        appointment = self.get_object()
        serializer = self.get_serializer(appointment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['POST'], detail=True, url_path='complete')
    def complete(self, request, pk=None):
        appointment = self.get_object()
        serializer = self.get_serializer(appointment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
