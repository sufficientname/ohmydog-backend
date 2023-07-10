from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from ohmydog import permissions
from ohmydog.campaigns.models import Campaign
from ohmydog.campaigns.serializers import (
    CampaignSerializer,
    CampaignCancelSerializer,
    CampaignCompleteSerializer,
    CampaignDonateSerializer,
    CampaignDonationSerializer,
)


class CampaignViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [permissions.IsCustomerUserOrReadOnly]

    def get_queryset(self):
        return Campaign.objects.all().order_by('start_date', 'end_date')
    
    def get_serializer_class(self):
        if self.action == 'donate':
            return CampaignDonateSerializer
        return CampaignSerializer

    @action(methods=['POST'], detail=True, url_path='donate', permission_classes=[])
    def donate(self, request, pk=None):
        campaign = self.get_object()
        serializer = self.get_serializer(campaign, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class CampaignAdminViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Campaign.objects.all().order_by('start_date', 'end_date')
    
    def get_serializer_class(self):
        if self.action == 'cancel':
            return CampaignCancelSerializer
        if self.action == 'complete':
            return CampaignCompleteSerializer
        if self.action == 'donations':
            return CampaignDonationSerializer
        return CampaignSerializer

    @action(methods=['POST'], detail=True, url_path='cancel')
    def cancel(self, request, pk=None):
        campaign = self.get_object()
        serializer = self.get_serializer(campaign, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['POST'], detail=True, url_path='complete')
    def complete(self, request, pk=None):
        campaign = self.get_object()
        serializer = self.get_serializer(campaign, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['GET'], detail=True, url_path='donations')
    def donations(self, request, pk=None):
        campaign = self.get_object()
        queryset = campaign.campaigndonation_set.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)