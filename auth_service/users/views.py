from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User, Role, Permission
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def update_me(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated, ]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def check_permission(request):
    permission_code = request.data.get("permission_code")

    if not permission_code:
        return Response({"detail": "permission_code is required"}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user

    has_permission = user.roles.filter(permissions__permission_code=permission_code).exists()

    return Response({
        "username": user.username,
        "permission_code": permission_code,
        "allowed": has_permission
    })
