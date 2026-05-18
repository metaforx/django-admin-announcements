from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import AdminAnnouncement


class AdminAnnouncementAdminMixin:
    list_display = ("version", "title", "starts_at", "expires_at", "is_published")
    list_filter = ("is_published", "groups")
    search_fields = ("version", "title", "summary", "body")
    ordering = ("-starts_at",)
    filter_horizontal = ("groups",)
    fieldsets = (
        (
            None,
            {
                "fields": [
                    "title",
                    "summary",
                    "body",
                    "version",
                ],
            },
        ),
        (
            _("Publication"),
            {
                "classes": ["tab"],
                "fields": [
                    "is_published",
                    "starts_at",
                    "expires_at",
                    "groups",
                ],
            },
        ),
    )


@admin.register(AdminAnnouncement)
class AdminAnnouncementAdmin(AdminAnnouncementAdminMixin, admin.ModelAdmin):
    pass
