from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from ohmydog.pets.models import Pet, HealthRecordEntry


class PetSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_fullname = serializers.SerializerMethodField()
    health_record = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = [
            'id',
            'user',
            'user_fullname',
            'name',
            'breed',
            'color',
            'birthdate',
            'health_record',
        ]

    def validate_name(self, value):
        user = self.context['request'].user
        if self.Meta.model.objects.filter(name=value, user=user).exists():
            raise serializers.ValidationError(_('Ya existe una mascota con este nombre.'))
        return value
    
    def get_user_fullname(self, instance: Pet):
        return f'{instance.user.first_name} {instance.user.last_name}'

    def get_health_record(self, instance: Pet):
        queryset = instance.healthrecordentry_set.all()
        return HealthRecordEntrySerializer(queryset, many=True).data


class HealthRecordEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecordEntry
        fields = [
            'id',
            'pet',
            'date',
            'entry_type',
            'entry_value',
        ]

