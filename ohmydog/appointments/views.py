import datetime

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from ohmydog import permissions
from ohmydog.appointments.models import Appointment
from ohmydog.appointments.serializers import (
    AppointmentSerializer,
    AppointmentRequestSerializer,
    AppointmentAcceptSerializer,
    AppointmentRejectSerializer,
    AppointmentCancelSerializer
)


class AppointmentViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    permission_classes = [permissions.IsCustomerUser]

    def get_queryset(self):
        user = self.request.user
        return Appointment.objects.filter(user=user).order_by('date')
    
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

    def get_queryset(self):
        today = datetime.date.today()
        return Appointment.objects.all().order_by('date')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AppointmentRequestSerializer
        if self.action == 'accept':
            return AppointmentAcceptSerializer
        if self.action == 'reject':
            return AppointmentRejectSerializer
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
