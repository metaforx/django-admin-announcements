"""Playwright UI tests for the admin announcement banner.

Run with: uv run pytest tests/test_ui_announcements.py --browser chromium -rs
"""

import pytest

from admin_announcements.models import AdminAnnouncement


@pytest.mark.django_db
@pytest.mark.ui
def test_banner_appears_for_staff(page, live_server, admin_user):
    admin_user.is_staff = True
    admin_user.save()
    AdminAnnouncement.objects.create(title="Notice", summary="UI test announcement", body="")
    page.goto(f"{live_server.url}/admin/")
    banner = page.locator("#announcements-banner")
    assert banner.is_visible()
    assert "UI test announcement" in banner.text_content()


@pytest.mark.django_db
@pytest.mark.ui
def test_banner_absent_without_announcements(page, live_server, admin_user):
    admin_user.is_staff = True
    admin_user.save()
    page.goto(f"{live_server.url}/admin/")
    banner = page.locator("#announcements-banner")
    assert banner.count() == 0


@pytest.mark.django_db
@pytest.mark.ui
def test_non_staff_does_not_see_banner(page, live_server, admin_user):
    admin_user.is_staff = False
    admin_user.save()
    AdminAnnouncement.objects.create(title="Hidden", summary="Should not see", body="")
    page.goto(f"{live_server.url}/admin/")
    assert page.url.startswith(f"{live_server.url}/admin/login/")
