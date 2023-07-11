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
    user_full_name = serializers.SerializerMethodField()
    user_discount_amount = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id',
            'user',
            'user_full_name',
            'user_discount_amount',
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
            'paid_amount',
            'discount_amount',
            'can_accept',
            'can_reject',
            'can_complete',
            'can_cancel',
        ]
    
    def get_pet_name(self, instance):
        return instance.pet.name
    
    def get_user_full_name(self, instance):
        return instance.user.full_name
    
    def get_user_discount_amount(self, instance):
        return instance.user.discount_amount
    

class AppointmentRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = [
            'pet',
            'reason',
            'date',
            'timeslot',
        ]

    def to_representation(self, instance):
        return AppointmentSerializer(instance, context=self.context).to_representation(instance)

    def validate_pet(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError(_('Esta mascota no te pertenece'))
        return value

    def create(self, validated_data):
        try:
            appointmet = self.Meta.model.objects.create_appointment_request(
                user=self.context['request'].user,
                pet=validated_data['pet'],
                reason=validated_data['reason'],
                date=validated_data['date'],
                timeslot=validated_data['timeslot']
            )
           
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
        instance.save()

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
            instance.apply_discount(instance.user.discount_amount)
            instance.save()

            instance.user.reset_discount_amount()
            instance.user.save()

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
        instance.save()
        return instance
