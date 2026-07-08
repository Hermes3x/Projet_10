from .permissions import IsSelfOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]

    def get_queryset(self):
        return User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
