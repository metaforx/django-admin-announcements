from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AdminAnnouncement(models.Model):
    version = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("version"),
        help_text=_("Optional release version reference (e.g. 2.0.0)"),
    )
    title = models.CharField(max_length=200, verbose_name=_("title"))
    summary = models.TextField(verbose_name=_("summary"))
    body = models.TextField(verbose_name=_("body"))
    starts_at = models.DateTimeField(default=timezone.now, verbose_name=_("starts at"))
    expires_at = models.DateTimeField(
        blank=True, null=True, verbose_name=_("expires at")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("active"))

    groups = models.ManyToManyField(
        "auth.Group",
        blank=True,
        related_name="admin_announcements",
        verbose_name=_("groups"),
        help_text=_("Restrict to users in these groups. Leave empty to show to all users."),
    )

    class Meta:
        verbose_name = _("admin announcement")
        verbose_name_plural = _("admin announcements")
        ordering = ["-starts_at"]

    def __str__(self):
        if self.version:
            return f"{self.version} — {self.title}"
        return self.title
