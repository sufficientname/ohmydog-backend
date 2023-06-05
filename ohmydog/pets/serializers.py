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
    user_fullname = serializers.SerializerMethodField()

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
        ]

    def get_user_fullname(self, instance):
        return f'{instance.user.first_name} {instance.user.last_name}'