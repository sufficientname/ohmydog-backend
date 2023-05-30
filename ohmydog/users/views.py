from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response


from ohmydog.users.models import User
from ohmydog.users.serializers import UserSerializer, UserPasswordSerializer


class UserMeApiView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class UserMePasswordApiView(generics.GenericAPIView):
    serializer_class = UserPasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=False).order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
