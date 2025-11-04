from rest_framework import permissions
from .models import RolePermission, UserRole


class HasPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        required_permission = getattr(view, 'required_permission', None)
        if not required_permission:
            return True

        user = request.user
        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        user_roles = UserRole.objects.filter(user=user).values_list('role', flat=True)
        perms = RolePermission.objects.filter(role_id__in=user_roles).values_list('permission__code', flat=True)
        return required_permission in perms
