from rest_framework import serializers
from .models import User, Permission, Role


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        # read_only_fields = [""]
        exclude = ["password", "groups", "user_permissions"]
