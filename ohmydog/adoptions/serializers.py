from rest_framework import serializers

from django.conf import settings

from django.core.mail import send_mail

from ohmydog.adoptions.models import AdoptionAd

class AdoptionAdSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pet_age = serializers.IntegerField(min_value=0)
    is_mine = serializers.SerializerMethodField()

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
            'Creaste un anuncio de adopcion en Oh my dog!',
            f'Los datos del anuncio son:\n nombre: {ad.pet_name}\n edad: {ad.pet_age}\n sexo: {ad.pet_gender}\n tamaño: {ad.pet_size}',
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
            raise serializers.ValidationError("Este anuncio no puede ser completado")
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
            raise serializers.ValidationError("Este anuncio no puede ser cancelado")
        return attrs

    def update(self, instance: AdoptionAd, validated_data):
        instance.cancel()
        self.instance.save()
        return instance