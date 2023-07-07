from rest_framework import serializers

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django.core.mail import send_mail

from ohmydog.serializer_fields import PhoneNumberField
from ohmydog.adoptions.models import AdoptionAd


class AdoptionAdSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pet_age = serializers.IntegerField(min_value=0)
    is_mine = serializers.SerializerMethodField()
    email = serializers.EmailField

    class Meta:
        model = AdoptionAd
        fields = [
            'id',
            'user',
            'user_id',
            'is_mine',
            'pet_name',
            'pet_age',
            'pet_gender',
            'pet_size',
            'status',
            'date_created',
            'can_complete',
            'can_cancel',
            'can_contact',
        ]
        read_only_fields = [
            'id',
            'user_id',
            'status',
            'date_created',
        ]
    
    def get_is_mine(self, instance: AdoptionAd):
        return instance.user == self.context['request'].user

    def create(self, validated_data):
        ad = super().create(validated_data)

        send_mail(
            _('Creaste un anuncio de adopcion en Oh my dog!'),
            _('Los datos del anuncio son:\n nombre: %(pet_name)s\n edad: %(pet_age)d\n sexo: %(pet_gender)s\n tamaño: %(pet_size)s')
                % dict(
                    pet_name=ad.pet_name,
                    pet_age=ad.pet_age,
                    pet_gender=ad.pet_gender,
                    pet_size=ad.pet_size
                ),
            settings.EMAIL_DEFAULT_FROM,
            [ad.user.email],
            fail_silently=True,
        )

        return ad


class AdoptionAdCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionAd
        fields = []

    def to_representation(self, instance):
        return AdoptionAdSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_complete():
            raise serializers.ValidationError(_('Este anuncio no puede ser completado'))
        return attrs

    def update(self, instance: AdoptionAd, validated_data):
        instance.complete()
        self.instance.save()
        return instance


class AdoptionAdCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionAd
        fields = []

    def to_representation(self, instance):
        return AdoptionAdSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_cancel():
            raise serializers.ValidationError(_('Este anuncio no puede ser cancelado'))
        return attrs

    def update(self, instance: AdoptionAd, validated_data):
        instance.cancel()
        self.instance.save()
        return instance


class AdoptionAdContactSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone_number = PhoneNumberField()
    reason = serializers.CharField()

    class Meta:
        model = AdoptionAd
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'reason',
        ]

    def to_representation(self, instance):
        return AdoptionAdSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_cancel():
            raise serializers.ValidationError(_('Este anuncio no puede ser contactado'))
        return attrs
    
    def update(self, instance: AdoptionAd, validated_data):
        send_mail(
            _('Le avisamos al anunciante que quieres ponerte en contacto con él por su anuncio de adopcion en Oh my dog!'),
            _('Los datos que proporcionaste para que el anunciante te contacte son:\n nombre: %(first_name)s\n apellido: %(last_name)s\n email: %(email)s\n telefono: %(phone_number)s\n motivo: %(reason)s')
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
            _('Alguien quiere contactase anuncio de adopcion en Oh my dog!'),
            _('Los datos del interesado son:\n nombre: %(first_name)s\n apellido: %(last_name)s\n email: %(email)s\n telefono: %(phone_number)s\n motivo: %(reason)s')
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