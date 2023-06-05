from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from ohmydog import permissions
from ohmydog.adoptions.models import AdoptionAd
from ohmydog.adoptions.serializers import AdoptionAdSerializer

class AdoptionAdViewSet(mixins.CreateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    permission_classes = [permissions.IsCustomerUserOrReadOnly]

    def get_queryset(self):
        return AdoptionAd.objects.all()
    
    def get_serializer_class(self):
        return AdoptionAdSerializer