from django.contrib import admin
from unfold.admin import ModelAdmin

import admin_announcements.admin  # noqa: F401  -- ensure default registration runs first
from admin_announcements.models import AdminAnnouncement

if AdminAnnouncement in admin.site._registry:
    admin.site.unregister(AdminAnnouncement)


@admin.register(AdminAnnouncement)
class AdminAnnouncementAdmin(ModelAdmin):
    list_display = ("version", "title", "starts_at", "expires_at", "is_active")
    list_filter = ("is_active", "groups")
    search_fields = ("version", "title", "summary", "body")
    ordering = ("-starts_at",)
    filter_horizontal = ("groups",)
