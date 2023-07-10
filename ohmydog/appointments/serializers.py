from rest_framework import serializers

from django.conf import settings
from django.db import transaction
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from ohmydog.appointments.models import Appointment
from ohmydog.appointments import constants
from ohmydog.appointments import exceptions


class AppointmentSerializer(serializers.ModelSerializer):
    pet_name = serializers.SerializerMethodField()
    user_fullname = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id',
            'user',
            'user_fullname',
            'pet',
            'pet_name',
            'reason',
            'date',
            'timeslot',
            'hour',
            'suggestion_date',
            'status',
            'observations',
            'days_to_booster',
            'booster_date',
            'observations',
            'price',
            'can_accept',
            'can_reject',
            'can_complete',
            'can_cancel',
        ]
    
    def get_pet_name(self, instance):
        return instance.pet.name
    
    def get_user_fullname(self, instance):
        return f'{instance.user.first_name} {instance.user.last_name}'
    

class AppointmentRequestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Appointment
        fields = [
            'pet',
            'user',
            'reason',
            'date',
            'timeslot',
        ]

    def to_representation(self, instance):
        return AppointmentSerializer(instance, context=self.context).to_representation(instance)

    def validate_pet(self, value):
        if value.user.id != self.context['request'].user.id:
            raise serializers.ValidationError(_('Esta mascota no te pertenece'))
        return value

    def create(self, validated_data):
        try:
            appointmet = self.Meta.model.objects.create_appointment_request(**validated_data)
           
            send_mail(
                _('Creaste una solicitud de turno en Oh my dog!'),
                _('Los datos del turno solicitado son:\n mascota: %(pet_name)s\n fecha: %(date)s\n motivo: %(reason)s\n franja horaria: %(timeslot)s')
                    % dict(
                        pet_name=appointmet.pet.name,
                        date=appointmet.date,
                        reason=appointmet.reason,
                        timeslot=appointmet.timeslot
                    ),
                settings.EMAIL_DEFAULT_FROM,
                [appointmet.user.email],
                fail_silently=True,
            )

            return appointmet

        except exceptions.BadReasonError as e:
            raise serializers.ValidationError({'non_field_errors': [str(e)]})


class AppointmentAcceptSerializer(serializers.ModelSerializer):
    hour = serializers.TimeField(required=True)
    
    class Meta:
        model = Appointment
        fields = [
            'hour',
        ]

    def to_representation(self, instance):
        return AppointmentSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_accept():
            raise serializers.ValidationError(_('Este turno no puede ser aceptado'))
        return attrs

    def update(self, instance: Appointment, validated_data):
        instance.accept(validated_data['hour'])
        instance.save()

        send_mail(
            _('Tu solicitud de turno en Oh my dog! fue aceptada'),
            _('Los datos del turno son:\n mascota: %(pet_name)s\n fecha: %(date)s\n motivo: %(reason)s\n hora: %(hour)s')
                % dict(
                    pet_name=instance.pet.name,
                    date=instance.date,
                    reason=instance.reason,
                    hour=instance.hour
                ),
            settings.EMAIL_DEFAULT_FROM,
            [instance.user.email],
            fail_silently=True,
        )
        
        return instance


class AppointmentRejectSerializer(serializers.ModelSerializer):
    suggestion_date = serializers.DateField(required=True)

    class Meta:
        model = Appointment
        fields = [
            'suggestion_date',
        ]
    
    def to_representation(self, instance):
        return AppointmentSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_reject():
            raise serializers.ValidationError(_('Este turno no puede ser rechazado'))
        return attrs

    def update(self, instance: Appointment, validated_data):
        instance.reject(validated_data['suggestion_date'])
        self.instance.save()

        send_mail(
            _('Tu solicutud de turno en Oh my dog! fue rechazada'),
            _('Tu solicitud de turno con los datos:\n mascota: %(pet_name)s\n fecha: %(date)s\n motivo: %(reason)s\n hora: %(hour)s\nfue rechazada.\nTe sugerimos que pidas un turno para la fecha: %(suggestion_date)s')
                % dict(
                    pet_name=instance.pet.name,
                    date=instance.date,
                    reason=instance.reason,
                    hour=instance.hour,
                    suggestion_date=instance.suggestion_date
                ),
            settings.EMAIL_DEFAULT_FROM,
            [instance.user.email],
            fail_silently=True,
        )

        return instance


class AppointmentCompleteSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=16 ,decimal_places=2, min_value=0)
    weight = serializers.DecimalField(max_digits=16, decimal_places=2, min_value=0)
    update_health_record = serializers.BooleanField()

    class Meta:
        model = Appointment
        fields = [
            'observations',
            'price',
            'weight',
            'update_health_record',
        ]

    def to_representation(self, instance):
        return AppointmentSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_complete():
            raise serializers.ValidationError(_('Este turno no puede ser completado'))
        return attrs

    def update(self, instance: Appointment, validated_data):
        with transaction.atomic():
            instance.complete(validated_data['price'], validated_data['observations'])
            self.instance.save()

            if validated_data['update_health_record']:
                health_record_entries = instance.make_health_record_entries(validated_data['weight'])
                if health_record_entries:
                    instance.pet.healthrecordentry_set.bulk_create(health_record_entries)

            return instance


class AppointmentCancelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = []

    def to_representation(self, instance):
        return AppointmentSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_cancel():
            raise serializers.ValidationError(_('Este turno no puede ser cancelado'))
        return attrs

    def update(self, instance: Appointment, validated_data):
        instance.cancel()
        self.instance.save()
        return instance
