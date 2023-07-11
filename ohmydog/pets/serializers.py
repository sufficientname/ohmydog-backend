from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from ohmydog.pets.models import Pet, HealthRecordEntry


class PetSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()
    health_record = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = [
            'id',
            'user',
            'user_full_name',
            'name',
            'breed',
            'gender',
            'color',
            'birthdate',
            'health_record',
        ]
    
    def get_user_full_name(self, instance: Pet):
        return instance.user.full_name

    def get_health_record(self, instance: Pet):
        queryset = instance.healthrecordentry_set.all()
        return HealthRecordEntrySerializer(queryset, many=True).data
    

class PetCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pet
        fields = [
            'name',
            'breed',
            'gender',
            'color',
            'birthdate',
        ]

    def to_representation(self, instance):
        return PetSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        user = self.context['request'].user
        if self.Meta.model.objects.filter(name=attrs['name'], user=user).exists():
            raise serializers.ValidationError(_('Ya existe una mascota con este nombre.'))
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class PetCreateAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pet
        fields = [
            'user',
            'name',
            'breed',
            'gender',
            'color',
            'birthdate',
        ]

    def to_representation(self, instance):
        return PetSerializer(instance, context=self.context).to_representation(instance)
    
    def validate(self, attrs):
        user = attrs['user']
        if self.Meta.model.objects.filter(name=attrs['name'], user=user).exists():
            raise serializers.ValidationError(_('Ya existe una mascota con este nombre.'))
        return attrs


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

