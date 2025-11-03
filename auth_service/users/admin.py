from django.contrib import admin

from users.models import User, Role, Permission, UserRole, RolePermission


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    pass
