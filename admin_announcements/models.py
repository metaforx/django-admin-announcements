from django.db import models


class AdminAnnouncement(models.Model):
    version = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    summary = models.TextField()
    body = models.TextField()
    starts_at = models.DateTimeField()
    expires_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        "auth.Group",
        blank=True,
        related_name="admin_announcements",
        help_text="Restrict to users in these groups. Leave empty to show to all users.",
    )

    class Meta:
        verbose_name = "Admin announcement"
        verbose_name_plural = "Admin announcements"
        ordering = ["-starts_at"]

    def __str__(self):
        return f"{self.version} — {self.title}"
