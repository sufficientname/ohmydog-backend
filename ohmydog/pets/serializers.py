from rest_framework import serializers
from ohmydog.pets.models import Pet


class PetSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Pet
        fields = [
            'id',
            'user',
            'name',
            'breed',
            'color',
            'birthdate',
        ]

class PetAdminSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pet
        fields = [
            'id',
            'user',
            'name',
            'breed',
            'color',
            'birthdate',
        ]