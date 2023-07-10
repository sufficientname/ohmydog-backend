from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action

from ohmydog import permissions
from ohmydog.advertisements.petsitters.models import PetSitterAd
from ohmydog.advertisements.petsitters.serializers import (
    PetSitterAdSerializer,
    PetSitterAdCancelSerializer,
    PetSitterAdCompleteSerializer,
    PetSitterAdContactSerializer,
    PetSitterAdPauseSerializer,
    PetSitterAdPauseRangeSerializer,
    PetSitterAdUnpauseSerializer,
)


class PetSitterAdViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = [permissions.IsCustomerUserOrReadOnly]
    filterset_fields = ['status']

    def get_queryset(self):
        PetSitterAd.pause_inrange_ads()
        PetSitterAd.unpause_inrage_ads()
        return PetSitterAd.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'contact':
            return PetSitterAdContactSerializer
        return PetSitterAdSerializer

    @action(methods=['POST'], detail=True, url_path='contact', permission_classes=[])
    def contact(self, request, pk=None):
        ad = self.get_object()
        if ad.user == request.user:
            raise PermissionDenied()
        serializer = self.get_serializer(ad, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PetSitterAdAdminViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['status']

    def get_queryset(self):
        PetSitterAd.pause_inrange_ads()
        PetSitterAd.unpause_inrage_ads()
        return PetSitterAd.objects.all()

    def get_serializer_class(self):
        if self.action == 'cancel':
            return PetSitterAdCancelSerializer
        if self.action == 'complete':
            return PetSitterAdCompleteSerializer
        if self.action == 'pause':
            return PetSitterAdPauseSerializer
        if self.action == 'pauserange':
            return PetSitterAdPauseRangeSerializer
        if self.action == 'unpause':
            return PetSitterAdUnpauseSerializer
        return PetSitterAdSerializer

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
    
    @action(methods=['POST'], detail=True, url_path='pause')
    def pause(self, request, pk=None):
        ad = self.get_object()
        serializer = self.get_serializer(ad, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(methods=['POST'], detail=True, url_path='pauserange')
    def pauserange(self, request, pk=None):
        ad = self.get_object()
        serializer = self.get_serializer(ad, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(methods=['POST'], detail=True, url_path='unpause')
    def unpause(self, request, pk=None):
        ad = self.get_object()
        serializer = self.get_serializer(ad, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)