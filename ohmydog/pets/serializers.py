from rest_framework import serializers
from ohmydog.pets.models import Pet


class PetSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    age = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = [
            'id',
            'user',
            'name',
            'breed',
            'color',
            'birthdate',
            'age',
        ]

    def get_age(self, instance: Pet):
        age = instance.age()
        return {'days': age.days, 'months': age.months, 'years': age.years}

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

    def get_user_fullname(self, instance: Pet):
        return f'{instance.user.first_name} {instance.user.last_name}'