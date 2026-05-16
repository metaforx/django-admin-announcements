from django.db import models
from django.db.models import Q
from django.utils import timezone


class AdminAnnouncementQuerySet(models.QuerySet):
    def active(self):
        now = timezone.now()
        return self.filter(is_active=True, starts_at__lte=now).filter(
            Q(expires_at__isnull=True) | Q(expires_at__gt=now)
        )

    def visible_to_user(self, user):
        if not user.is_authenticated or not user.is_staff:
            return self.none()

        user_group_ids = user.groups.values_list("pk", flat=True) if user.pk else []
        return self.active().filter(
            Q(groups__isnull=True) | Q(groups__in=user_group_ids)
        ).distinct()
