from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from ohmydog import permissions
from ohmydog.adoptions.models import AdoptionAd
from ohmydog.adoptions.serializers import (
    AdoptionAdSerializer,
    AdoptionAdCancelSerializer,
    AdoptionAdCompleteSerializer
)

class AdoptionAdViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    permission_classes = [permissions.IsCustomerUserOrReadOnly]

    def get_queryset(self):
        return AdoptionAd.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'cancel':
            return AdoptionAdCancelSerializer
        if self.action == 'complete':
            return AdoptionAdCompleteSerializer
        return AdoptionAdSerializer
    
    @action(methods=['POST'], detail=True, url_path='cancel')
    def cancel(self, request, pk=None):
        ad = self.get_object()
        serializer = self.get_serializer(ad, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(methods=['POST'], detail=True, url_path='complete')
    def complete(self, request, pk=None):
        ad = self.get_object()
        serializer = self.get_serializer(ad, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)