from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class JWTCBATokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT Claim-Based Authorization Token Serializer
    """
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        roles = list(user.roles.values_list("role_name", flat=True))
        permissions = list(
            user.roles.values_list("permissions__permission_code", flat=True)
        )

        token["roles"] = roles
        token["permissions"] = permissions
        token["username"] = user.username

        return token