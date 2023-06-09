from rest_framework import serializers

from django.conf import settings

from django.core.mail import send_mail

from ohmydog.adoptions.models import AdoptionAd

class AdoptionAdSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = AdoptionAd
        fields = [
            'id',
            'user',
            'user_id',
            'pet_name',
            'pet_age',
            'pet_gender',
            'pet_size',
            'status',
            'date_created',
        ]
        read_only_fields = [
            'id',
            'user_id',
            'status',
            'date_created',
        ]
    
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