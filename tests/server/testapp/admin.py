from django.contrib import admin
from django.contrib.auth.models import Group, User

try:
    from unfold.admin import ModelAdmin as AdminBase
except ImportError:
    AdminBase = admin.ModelAdmin


class UserAdmin(AdminBase):
    list_display = ("username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active", "is_superuser")


class GroupAdmin(AdminBase):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
