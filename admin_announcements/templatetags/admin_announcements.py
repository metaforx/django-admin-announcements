import markdown as markdown_lib
from django import template
from django.utils.safestring import mark_safe

from admin_announcements.models import AdminAnnouncement

register = template.Library()


@register.inclusion_tag("admin_announcements/announcements_banner.html", takes_context=True)
def admin_announcements_banner(context):
    request = context.get("request")
    if request is None:
        return {"active_announcements": []}
    return {
        "active_announcements": AdminAnnouncement.objects.visible_to_user(request.user),
    }


@register.filter(name="markdown")
def markdown(value):
    return mark_safe(markdown_lib.markdown(value or "", extensions=["extra"]))
