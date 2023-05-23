from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action

from ohmydog.pets.models import Pet
from ohmydog.pets.serializers import PetSerializer, PetAdminSerializer

class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Pet.objects.filter(user_id=user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PetAdminViewSet(viewsets.ModelViewSet):
    serializer_class = PetAdminSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Pet.objects.all()