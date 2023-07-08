from rest_framework import viewsets
from rest_framework.decorators import action

from ohmydog import permissions
from ohmydog.pets.models import Pet
from ohmydog.pets.serializers import PetSerializer, PetAdminSerializer

class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [permissions.IsCustomerUser]

    def get_queryset(self):
        user = self.request.user
        return Pet.objects.filter(user=user)


class PetAdminViewSet(viewsets.ModelViewSet):
    serializer_class = PetAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ['user']

    def get_queryset(self):
        return Pet.objects.all()