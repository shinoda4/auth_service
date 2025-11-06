from django_filters.rest_framework import DjangoFilterBackend
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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'email', 'phone_number']
    search_fields = ['username', 'email', 'phone_number']  # 模糊搜索
    ordering_fields = ['username', 'email', 'phone_number']  # 排序


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    filterset_fields = ['role_name']
    search_fields = ['role_name']  # 模糊搜索
    ordering_fields = ['role_name']  # 排序


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    filterset_fields = ['permission_code', 'permission_name']
    search_fields = ['permission_code', 'permission_name']  # 模糊搜索
    ordering_fields = ['permission_code', 'permission_name']  # 排序


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def check_permission(request):
    user = request.user

    permission_code = request.data.get("permission_code")

    if not permission_code and not user.is_superuser:
        return Response({"detail": "permission_code is required"}, status=status.HTTP_400_BAD_REQUEST)
    elif not permission_code and user.is_superuser:
        return Response({"detail": {"is_superuser": True}}, status=status.HTTP_200_OK)

    has_permission = user.roles.filter(permissions__permission_code=permission_code).exists()

    return Response({
        "username": user.username,
        "permission_code": permission_code,
        "allowed": has_permission
    })
