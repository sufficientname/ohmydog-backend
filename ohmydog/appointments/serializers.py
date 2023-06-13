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
        if value.user_id != self.context['request'].user.id:
            raise serializers.ValidationError("invalid pet")
        return value

    def create(self, validated_data):
        try:
            return self.Meta.model.objects.create_appointment_request(**validated_data)
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
            raise serializers.ValidationError("Este turno no puede ser aprobado")
        return attrs

    def update(self, instance: Appointment, validated_data):
        instance.accept(validated_data['hour'])
        instance.save()
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
            raise serializers.ValidationError("Este turno no puede ser rechazado")
        return attrs

    def update(self, instance: Appointment, validated_data):
        instance.reject(validated_data['suggestion_date'])
        self.instance.save()
        return instance


class AppointmentCompleteSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=16 ,decimal_places=2, min_value=0)

    class Meta:
        model = Appointment
        fields = [
            'price',
            'observations'
        ]

    def to_representation(self, instance):
        return AppointmentSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_complete():
            raise serializers.ValidationError("Este turno no puede ser completado")
        return attrs

    def update(self, instance: Appointment, validated_data):
        instance.complete(validated_data['price'], validated_data['observations'])
        self.instance.save()
        return instance


class AppointmentCancelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = []

    def to_representation(self, instance):
        return AppointmentSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_cancel():
            raise serializers.ValidationError("Este turno no puede ser cancelado")
        return attrs

    def update(self, instance: Appointment, validated_data):
        instance.cancel()
        self.instance.save()
        return instance
