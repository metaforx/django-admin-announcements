from django import template
from django.template.defaultfilters import linebreaksbr
from django.utils.safestring import mark_safe

from admin_announcements.models import AdminAnnouncement

try:
    import markdown as markdown_lib
except ImportError:
    markdown_lib = None

try:
    import nh3
except ImportError:
    nh3 = None


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
    if not value:
        return ""
    # Without a sanitizer we refuse to emit HTML — fall back to escaped text.
    if markdown_lib is None or nh3 is None:
        return linebreaksbr(value)
    return mark_safe(nh3.clean(markdown_lib.markdown(value, extensions=["extra"])))
