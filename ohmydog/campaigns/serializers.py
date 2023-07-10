from rest_framework import serializers

from django.db import transaction
from django.utils.translation import gettext_lazy as _

import decimal

from ohmydog.serializer_fields import PhoneNumberField
from ohmydog.campaigns.models import Campaign, CampaignDonation


class CampaignSerializer(serializers.ModelSerializer):
    donations = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            'id',
            'status',
            'name',
            'description',
            'start_date',
            'end_date',
            'goal_amount',
            'current_amount',
            'can_donate',
            'can_cancel',
            'can_complete',
            'donations',
        ]
        read_only_fields = [
            'id',
            'status',
            'start_date',
            'current_amount',
            'donations',
        ]

    def get_donations(self, instance: Campaign):
        if self.context['request'].user.is_staff:
            queryset = instance.campaigndonation_set
            return CampaignDonationSerializer(queryset, many=True).data
        return []


class CampaignCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = []
    
    def to_representation(self, instance):
        return CampaignSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_cancel():
            raise serializers.ValidationError(_('Esta campaña no puede ser cancelada'))
        return attrs

    def update(self, instance: Campaign, validated_data):
        instance.cancel()
        self.instance.save()
        return instance


class CampaignCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = []
    
    def to_representation(self, instance):
        return CampaignSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_complete():
            raise serializers.ValidationError(_('Esta campaña no puede ser completada'))
        return attrs

    def update(self, instance: Campaign, validated_data):
        instance.complete()
        self.instance.save()
        return instance


class CampaignDonateSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=decimal.Decimal('0.01'))
    donor_first_name = serializers.CharField(max_length=150)
    donor_last_name = serializers.CharField(max_length=150)
    donor_email = serializers.EmailField()
    donor_phone_number = PhoneNumberField()

    class Meta:
        model = CampaignDonation
        fields = [
            'amount',
            'donor_first_name',
            'donor_last_name',
            'donor_email',
            'donor_phone_number',
        ]

    def to_representation(self, instance):
        return CampaignSerializer(instance, context=self.context).to_representation(instance)

    def validate(self, attrs):
        if not self.instance.can_donate():
            raise serializers.ValidationError(_('Esta campaña no puede recibir donaciones'))
        return attrs

    def update(self, instance: Campaign, validated_data):
        with transaction.atomic():
            donation = instance.make_donation(
                amount=validated_data['amount'],
                donor_first_name=validated_data['donor_first_name'],
                donor_last_name=validated_data['donor_last_name'],
                donor_email=validated_data['donor_email'],
                donor_phone_number=validated_data['donor_phone_number'],
            )
            if donation is not None:
                donation.save()
            instance.save()
            return instance


class CampaignDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignDonation
        fields = [
            'id',
            'campaign',
            'amount',
            'donor_first_name',
            'donor_last_name',
            'donor_email',
            'donor_phone_number',
            'created_at',
        ]