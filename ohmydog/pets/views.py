from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from ohmydog import permissions
from ohmydog.pets.models import Pet
from ohmydog.pets.serializers import (
    PetSerializer,
    PetCreateSerializer,
    PetCreateAdminSerializer,
    HealthRecordEntrySerializer
)

class PetViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsCustomerUser]

    def get_queryset(self):
        user = self.request.user
        return Pet.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PetCreateSerializer
        if self.action == 'healthrecord':
            return HealthRecordEntrySerializer
        return PetSerializer
    
    @action(methods=['GET'], detail=True, url_path='healthrecord')
    def healthrecord(self, request, pk=None):
        pet = self.get_object()
        queryset = pet.healthrecordentry_set.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PetAdminViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['user']

    def get_queryset(self):
        return Pet.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return PetCreateAdminSerializer
        if self.action == 'healthrecord':
            return HealthRecordEntrySerializer
        return PetSerializer

    @action(methods=['GET'], detail=True, url_path='healthrecord')
    def healthrecord(self, request, pk=None):
        pet = self.get_object()
        queryset = pet.healthrecordentry_set.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)