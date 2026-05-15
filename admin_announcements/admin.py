from django.contrib import admin

from .models import AdminAnnouncement


@admin.register(AdminAnnouncement)
class AdminAnnouncementAdmin(admin.ModelAdmin):
    list_display = ("version", "title", "starts_at", "expires_at", "is_active")
    list_filter = ("is_active", "groups")
    search_fields = ("version", "title", "summary", "body")
    ordering = ("-starts_at",)
    filter_horizontal = ("groups",)
