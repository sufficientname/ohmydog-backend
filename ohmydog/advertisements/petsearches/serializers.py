from rest_framework import serializers

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django.core.mail import send_mail

from ohmydog.serializer_fields import PhoneNumberField
from ohmydog.advertisements.petsearches.models import PetSearchAd


class PetSearchAdSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_mine = serializers.SerializerMethodField()
    pet_age = serializers.IntegerField(min_value=0)
    # pet_photo = serializers.ImageField(required=False, use_url=True)

    class Meta:
        model = PetSearchAd
        fields = [
            'id',
            'user',
            'status',
            'date_created',
            'pet_name',
            'pet_age',
            'pet_gender',
            'pet_breed',
            'pet_size',
            'pet_color',
            'last_seen_area',
            # 'pet_photo',
            'can_complete',
            'can_cancel',
            'can_contact',
            'is_mine',
        ]
        read_only_fields = [
            'id',
            'status',
            'date_created',
        ]
    
    def get_is_mine(self, instance: PetSearchAd):
        return instance.user == self.context['request'].user

    def create(self, validated_data):
        ad = super().create(validated_data)

        send_mail(
            _('Creaste un anuncio de busqueda de perro perdido en Oh my dog!'),
            _('Los datos del anuncio son:\n nombre: %(pet_name)s\n edad: %(pet_age)d\n sexo: %(pet_gender)s\n raza: %(pet_breed)s\n zona: %(last_seen_area)s')
                % dict(
                    pet_name=ad.pet_name,
                    pet_age=ad.pet_age,
                    pet_gender=ad.pet_gender,
                    pet_breed=ad.pet_breed,
                    last_seen_area=ad.last_seen_area,
                ),
            settings.EMAIL_DEFAULT_FROM,
            [ad.user.email],
            fail_silently=True,
        )

        return ad


class PetSearchAdCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetSearchAd
        fields = []

    def to_representation(self, instance):
        return PetSearchAdSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_complete():
            raise serializers.ValidationError(_('Este anuncio no puede ser completado'))
        return attrs

    def update(self, instance: PetSearchAd, validated_data):
        instance.complete()
        self.instance.save()
        return instance


class PetSearchAdCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetSearchAd
        fields = []

    def to_representation(self, instance):
        return PetSearchAdSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_cancel():
            raise serializers.ValidationError(_('Este anuncio no puede ser cancelado'))
        return attrs

    def update(self, instance: PetSearchAd, validated_data):
        instance.cancel()
        self.instance.save()
        return instance


class PetSearchAdContactSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone_number = PhoneNumberField()
    reason = serializers.CharField()

    class Meta:
        model = PetSearchAd
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'reason',
        ]

    def to_representation(self, instance):
        return PetSearchAdSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_contact():
            raise serializers.ValidationError(_('Este anuncio no puede ser contactado'))
        return attrs
    
    def update(self, instance: PetSearchAd, validated_data):
        send_mail(
            _('Le avisamos al anunciante que quieres ponerte en contacto con el por su anuncio de busqueda de perro perdido en Oh my dog!'),
            _('Los datos que proporcionaste para que el anunciante te contacte son:\n nombre: %(first_name)s\n apellido: %(last_name)s\n email: %(email)s\n teléfono: %(phone_number)s\n motivo: %(reason)s')
                % dict(
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    email=validated_data['email'],
                    phone_number=validated_data['phone_number'],
                    reason=validated_data['reason']
                ),
            settings.EMAIL_DEFAULT_FROM,
            [validated_data['email']],
            fail_silently=True,
        )

        send_mail(
            _('Alguien quiere contactase con vos por tu anuncio de busqueda de perro perdido en Oh my dog!'),
            _('Los datos del interesado son:\n nombre: %(first_name)s\n apellido: %(last_name)s\n email: %(email)s\n teléfono: %(phone_number)s\n motivo: %(reason)s')
                % dict(
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    email=validated_data['email'],
                    phone_number=validated_data['phone_number'],
                    reason=validated_data['reason']
                ),
            settings.EMAIL_DEFAULT_FROM,
            [instance.user.email],
            fail_silently=True,
        )

        return instance