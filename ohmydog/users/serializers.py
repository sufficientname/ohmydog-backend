from rest_framework import serializers
from django.contrib.auth import authenticate, update_session_auth_hash

from django.core.mail import send_mail

from ohmydog.users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'id_number',
        ]
        read_only_fields = [
            'is_staff',
        ]

    def create(self, validated_data):
        password = make_random_password()

        user = self.Meta.model.objects.create_user(
            validated_data['email'],
            email=validated_data['email'],
            password=password,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            id_number=validated_data['id_number']
        )

        send_mail(
            'Bienvenido a Oh my dog!',
            f'Su contraseña es {password}',
            "contacto@ohmydog.com.ar",
            [user.email],
            fail_silently=True,
        )

        return user

class UserPasswordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'password',
        ]

    def to_representation(self, instance):
        return UserSerializer(instance).to_representation(instance)

    def create(self, validated_data):
        raise NotImplementedError('`create()` must be implemented.')

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        request = self.context.get('request', None)
        if request is not None:
            update_session_auth_hash(request, request.user)
        return instance


def make_random_password():
    return "12345"

