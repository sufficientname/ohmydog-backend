from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action

from ohmydog import permissions
from ohmydog.advertisements.petsearches.models import PetSearchAd
from ohmydog.advertisements.petsearches.serializers import (
    PetSearchAdSerializer,
    PetSearchAdCancelSerializer,
    PetSearchAdCompleteSerializer,
    PetSearchAdContactSerializer,
)


class PetSearchAdViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    permission_classes = [permissions.IsCustomerUserOrReadOnly]
    filterset_fields = ['user', 'status']

    def get_queryset(self):
        return PetSearchAd.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'cancel':
            return PetSearchAdCancelSerializer
        if self.action == 'complete':
            return PetSearchAdCompleteSerializer
        if self.action == 'contact':
            return PetSearchAdContactSerializer
        return PetSearchAdSerializer

    @action(methods=['POST'], detail=True, url_path='cancel')
    def cancel(self, request, pk=None):
        ad = self.get_object()
        if ad.user != request.user:
            raise PermissionDenied()
        serializer = self.get_serializer(ad, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(methods=['POST'], detail=True, url_path='complete')
    def complete(self, request, pk=None):
        ad = self.get_object()
        if ad.user != request.user:
            raise PermissionDenied()
        serializer = self.get_serializer(ad, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['POST'], detail=True, url_path='contact', permission_classes=[])
    def contact(self, request, pk=None):
        ad = self.get_object()
        if ad.user == request.user:
            raise PermissionDenied()
        serializer = self.get_serializer(ad, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PetSearchAdAdminViewSet(mixins.RetrieveModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['user', 'status']

    def get_queryset(self):
        return PetSearchAd.objects.all()

    def get_serializer_class(self):
        return PetSearchAdSerializer