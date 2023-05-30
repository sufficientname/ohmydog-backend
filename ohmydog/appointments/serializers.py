from rest_framework import serializers
from ohmydog.appointments.models import Appointment
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
            'pet_id',
            'pet_name',
            'reason',
            'request_date',
            'request_timeslot',
            'actual_datetime',
            'suggestion_datetime',
            'status',
            'observations',
            'days_to_booster',
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
            'request_date',
            'request_timeslot',
        ]

    def to_representation(self, instance):
        return AppointmentSerializer(instance).to_representation(instance)

    def validate_pet(self, value):
        if value.user_id != self.context['request'].user.id:
            raise serializers.ValidationError("invalid pet")
        return value

    def create(self, validated_data):
        try:
            return self.Meta.model.objects.create_appointment_request(**validated_data)
        except exceptions.BadReasonError as e:
            raise serializers.ValidationError(str(e))

class AppointmentActionSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return AppointmentSerializer(instance).to_representation(instance)

    def create(self, validated_data):
        raise NotImplementedError('`create()` must be implemented.')


class AppointmentApproveSerializer(AppointmentActionSerializer):
    actual_datetime = serializers.DateTimeField(required=True)
    
    class Meta:
        model = Appointment
        fields = [
            'actual_datetime',
        ]

    def update(self, instance: Appointment, validated_data):
        instance.approve(self.validated_data['actual_datetime'])
        instance.save()
        return instance


class AppointmentRejectSerializer(AppointmentActionSerializer):
    suggestion_datetime = serializers.DateTimeField(required=True)

    class Meta:
        model = Appointment
        fields = [
            'suggestion_datetime'
        ]

    def update(self, instance: Appointment, validated_data):
        instance.reject(self.validated_data['suggestion_datetime'])
        self.instance.save()
        return instance

class AppointmentCancelSerializer(AppointmentActionSerializer):

    class Meta:
        model = Appointment
        fields = []

    def update(self, instance: Appointment, validated_data):
        instance.cancel()
        self.instance.save()
        return instance