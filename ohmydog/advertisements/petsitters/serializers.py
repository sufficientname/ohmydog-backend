from rest_framework import serializers

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django.core.mail import send_mail

from ohmydog.serializers import PhoneNumberField
from ohmydog.advertisements.petsitters.models import PetSitterAd


class PetSitterAdSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_mine = serializers.SerializerMethodField()
    sitter_phone_number = PhoneNumberField()

    class Meta:
        model = PetSitterAd
        fields = [
            'id',
            'user',
            'status',
            'created_at',
            'sitter_first_name',
            'sitter_last_name',
            'sitter_email',
            'sitter_phone_number',
            'service_type',
            'service_area',
            'pause_start_date',
            'pause_end_date',
            'can_complete',
            'can_cancel',
            'can_contact',
            'can_pause',
            'can_unpause',
            'is_mine',
        ]
        read_only_fields = [
            'id',
            'status',
            'created_at',
        ]
    
    def get_is_mine(self, instance: PetSitterAd):
        return instance.user == self.context['request'].user

    def create(self, validated_data):
        ad = super().create(validated_data)
        send_mail(
            _('Tu anuncio de servicio de paseadores o cuidadores fue publicado en Oh my dog!'),
            _('Los datos del anuncio son:\n nombre: %(sitter_first_name)s\n apellido: %(sitter_last_name)s\n email: %(sitter_email)s\n telefono: %(sitter_phone_number)s\n servicio: %(service_type)s\n zona: %(service_area)s')
                % dict(
                    sitter_first_name=ad.sitter_first_name,
                    sitter_last_name=ad.sitter_last_name,
                    sitter_email=ad.sitter_email,
                    sitter_phone_number=ad.sitter_phone_number,
                    service_type=ad.service_type,
                    service_area=ad.service_area,
                ),
            settings.EMAIL_DEFAULT_FROM,
            [ad.sitter_email],
            fail_silently=True,
        )

        return ad


class PetSitterAdCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetSitterAd
        fields = []

    def to_representation(self, instance):
        return PetSitterAdSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_complete():
            raise serializers.ValidationError(_('Este anuncio no puede ser completado'))
        return attrs

    def update(self, instance: PetSitterAd, validated_data):
        instance.complete()
        instance.save()
        return instance


class PetSitterAdCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetSitterAd
        fields = []

    def to_representation(self, instance):
        return PetSitterAdSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_cancel():
            raise serializers.ValidationError(_('Este anuncio no puede ser cancelado'))
        return attrs

    def update(self, instance: PetSitterAd, validated_data):
        instance.cancel()
        instance.save()
        return instance


class PetSitterAdContactSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    phone_number = PhoneNumberField()
    reason = serializers.CharField()

    class Meta:
        model = PetSitterAd
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'reason',
        ]

    def to_representation(self, instance):
        return PetSitterAdSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_contact():
            raise serializers.ValidationError(_('Este anuncio no puede ser contactado'))
        return attrs
    
    def update(self, instance: PetSitterAd, validated_data):
        send_mail(
            _('Le avisamos al anunciante que quieres ponerte en contacto con el por su anuncio de cuidador en Oh my dog!'),
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
            [instance.sitter_email],
            fail_silently=True,
        )

        return instance


class PetSitterAdPauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetSitterAd
        fields = []

    def to_representation(self, instance):
        return PetSitterAdSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_pause():
            raise serializers.ValidationError(_('Este anuncio no puede ser pausado'))
        return attrs

    def update(self, instance: PetSitterAd, validated_data):
        instance.pause()
        instance.save()
        return instance


class PetSitterAdPauseRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetSitterAd
        fields = [
            'pause_start_date',
            'pause_end_date',
        ]

    def to_representation(self, instance):
        return PetSitterAdSerializer(instance, context=self.context).to_representation(instance)
    
    def validate(self, attrs):
        if attrs['pause_start_date'] > attrs['pause_end_date']:
            raise serializers.ValidationError(_('La fecha de inicio de pausa debe ser anterior a la fecha de fin de pausa'))

        if not self.instance.can_pause():
            raise serializers.ValidationError(_('Este anuncio no puede ser pausado'))

        return attrs

    def update(self, instance: PetSitterAd, validated_data):
        instance.pause_range(
            validated_data['pause_start_date'],
            validated_data['pause_end_date'],
        )
        instance.save()
        return instance

class PetSitterAdUnpauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetSitterAd
        fields = []

    def to_representation(self, instance):
        return PetSitterAdSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_unpause():
            raise serializers.ValidationError(_('Este anuncio no puede ser despausado'))
        return attrs

    def update(self, instance: PetSitterAd, validated_data):
        instance.unpause()
        instance.save()
        return instance