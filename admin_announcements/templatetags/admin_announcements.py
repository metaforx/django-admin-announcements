from django import template
from django.template.defaultfilters import linebreaksbr
from django.utils.safestring import mark_safe

from admin_announcements.models import AdminAnnouncement

try:
    import markdown as markdown_lib
except ImportError:
    markdown_lib = None


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
    if markdown_lib is None:
        return linebreaksbr(value or "")
    return mark_safe(markdown_lib.markdown(value or "", extensions=["extra"]))
