from django.contrib.admin import site as admin_site
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import AdminAnnouncement


@staff_member_required
def announcement_detail(request, pk):
    user_group_ids = list(request.user.groups.values_list("pk", flat=True))
    qs = AdminAnnouncement.objects.filter(
        Q(groups__isnull=True) | Q(groups__in=user_group_ids)
    ).distinct()
    announcement = get_object_or_404(qs, pk=pk)
    context = admin_site.each_context(request)
    context["announcement"] = announcement
    context["title"] = str(announcement)
    return render(
        request,
        "admin_announcements/announcement_detail.html",
        context,
    )
