# users/views.py
from xmlrpc.client import Fault

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Role, Permission, UserRole, RolePermission
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer, UserRoleSerializer, \
    RolePermissionSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def roles_permissions(self, request, pk=None):
        user = self.get_object()
        roles = [ur.role.name for ur in user.roles.all()]
        permissions = []
        for ur in user.roles.all():
            perms = RolePermission.objects.filter(role=ur.role)
            permissions.extend([p.permission.code for p in perms])
        return Response({
            'user_id': user.id,
            'username': user.username,
            'roles': roles,
            'permissions': list(set(permissions))
        })


# Role CRUD
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]


# Permission CRUD
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['delete'])
    def delete_by_user_role(self, request):
        user_id = request.data.get('user_id')
        role_id = request.data.get('role_id')
        try:
            obj = UserRole.objects.get(user_id=user_id, role_id=role_id)
            obj.delete()
            return Response({'status': 'deleted'}, status=status.HTTP_200_OK)
        except UserRole.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['delete'])
    def delete_by_role_permission(self, request):
        role_id = request.data.get('role_id')
        permission_id = request.data.get('permission_id')
        try:
            obj = RolePermission.objects.get(role_id=role_id, permission_id=permission_id)
            obj.delete()
            return Response({'status': 'deleted'}, status=status.HTTP_200_OK)
        except RolePermission.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
