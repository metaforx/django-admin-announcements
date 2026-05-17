from django.contrib.admin import site as admin_site
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.clickjacking import xframe_options_sameorigin

from .models import AdminAnnouncement


@staff_member_required
@xframe_options_sameorigin
def announcement_detail(request, pk):
    qs = AdminAnnouncement.objects.visible_to_user(request.user)
    announcement = get_object_or_404(qs, pk=pk)
    context = admin_site.each_context(request)
    context["announcement"] = announcement
    context["is_popup"] = IS_POPUP_VAR in request.GET or IS_POPUP_VAR in request.POST
    context["title"] = str(announcement)
    return render(
        request,
        "admin_announcements/announcement_detail.html",
        context,
    )
