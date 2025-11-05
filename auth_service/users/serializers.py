from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from djoser.serializers import UserCreatePasswordRetypeSerializer as BaseUserCreatePasswordRetypeSerializer

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


class UserCreateSerializer(BaseUserCreatePasswordRetypeSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone_number = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    re_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta(BaseUserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'password', 're_password')
