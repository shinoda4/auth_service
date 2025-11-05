from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

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

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if not request or not request.user.is_superuser:
            fields.pop("is_superuser", None)
            fields.pop("is_staff", None)
        return fields

    class Meta:
        model = User
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


class UserCreateSerializer(BaseUserCreateSerializer):
    phone_number = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)
    re_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'password', 're_password')

    def validate(self, attrs):
        print(attrs)
        if not attrs.get("phone_number"):
            raise serializers.ValidationError({"phone_number": "This field is required."})
        if not attrs.get("email"):
            raise serializers.ValidationError({"email": "This field is required."})
        return attrs
