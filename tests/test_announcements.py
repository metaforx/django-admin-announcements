from datetime import timedelta

import pytest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, Group, User
from django.template.loader import get_template
from django.utils import timezone

from admin_announcements.models import AdminAnnouncement


def assert_empty_result(result):
    assert list(result) == []


@pytest.mark.django_db
class TestAdminAnnouncementQuerySet:
    def test_empty_for_anonymous(self):
        assert_empty_result(AdminAnnouncement.objects.visible_to_user(AnonymousUser()))

    def test_empty_for_non_staff(self):
        user = User(username="u", is_staff=False)
        assert_empty_result(AdminAnnouncement.objects.visible_to_user(user))

    def test_returns_active(self):
        user = User(username="u", is_staff=True)
        AdminAnnouncement.objects.create(title="A", summary="S", body="B")
        result = AdminAnnouncement.objects.visible_to_user(user)
        assert len(result) == 1

    def test_excludes_inactive(self):
        user = User(username="u", is_staff=True)
        AdminAnnouncement.objects.create(
            title="A", summary="S", body="B", is_active=False
        )
        assert_empty_result(AdminAnnouncement.objects.visible_to_user(user))

    def test_excludes_expired(self):
        user = User(username="u", is_staff=True)
        AdminAnnouncement.objects.create(
            title="A",
            summary="S",
            body="B",
            expires_at=timezone.now() - timedelta(hours=1),
        )
        assert_empty_result(AdminAnnouncement.objects.visible_to_user(user))

    def test_excludes_future(self):
        user = User(username="u", is_staff=True)
        AdminAnnouncement.objects.create(
            title="A",
            summary="S",
            body="B",
            starts_at=timezone.now() + timedelta(days=1),
        )
        assert_empty_result(AdminAnnouncement.objects.visible_to_user(user))

    def test_filters_by_group(self):
        group = Group.objects.create(name="editors")
        user = User(username="u", is_staff=True)
        user.save()
        a = AdminAnnouncement.objects.create(title="A", summary="S", body="B")
        a.groups.add(group)

        assert_empty_result(AdminAnnouncement.objects.visible_to_user(user))

    def test_shows_when_in_group(self):
        group = Group.objects.create(name="editors")
        user = User(username="u", is_staff=True)
        user.save()
        user.groups.add(group)
        a = AdminAnnouncement.objects.create(title="A", summary="S", body="B")
        a.groups.add(group)

        result = AdminAnnouncement.objects.visible_to_user(user)
        assert len(result) == 1


@pytest.mark.django_db
class TestBannerRendersInAdmin:
    def _skip_if_unfold(self):
        if getattr(settings, "ADMIN_ANNOUNCEMENTS_TESTS_UNFOLD", False):
            pytest.skip(
                "Banner rendering is tested with default settings (Unfold uses its own templates)"
            )

    def test_banner_present_with_announcement(self, admin_client):
        self._skip_if_unfold()
        AdminAnnouncement.objects.create(title="Notify", summary="Hello", body="")
        response = admin_client.get("/admin/")
        assert response.status_code == 200
        assert b"announcements-banner" in response.content
        assert b"Notify" in response.content

    def test_banner_renders_before_admin_header(self, admin_client):
        self._skip_if_unfold()
        AdminAnnouncement.objects.create(title="Notify", summary="Hello", body="")
        response = admin_client.get("/admin/")
        banner_index = response.content.index(b'id="announcements-banner"')
        header_index = response.content.index(b'id="header"')
        assert banner_index < header_index

    def test_banner_absent_without_announcement(self, admin_client):
        self._skip_if_unfold()
        response = admin_client.get("/admin/")
        assert b"announcements-banner" not in response.content

    def test_banner_links_to_detail(self, admin_client):
        self._skip_if_unfold()
        a = AdminAnnouncement.objects.create(title="X", summary="Detail link", body="")
        response = admin_client.get("/admin/")
        url = f"/admin/announcements/detail/{a.pk}/"
        assert url.encode() in response.content

    def test_expired_not_in_banner(self, admin_client):
        self._skip_if_unfold()
        AdminAnnouncement.objects.create(
            title="Old",
            summary="Gone",
            body="",
            expires_at=timezone.now() - timedelta(days=1),
        )
        response = admin_client.get("/admin/")
        assert b"announcements-banner" not in response.content


@pytest.mark.django_db
class TestBannerRendersInUnfoldAdmin:
    def _skip_unless_unfold(self):
        if not getattr(settings, "ADMIN_ANNOUNCEMENTS_TESTS_UNFOLD", False):
            pytest.skip("Unfold banner rendering requires Unfold settings")

    def test_unfold_template_override_is_used(self):
        self._skip_unless_unfold()
        for template_name in ["admin/base.html", "admin/index.html"]:
            template = get_template(template_name)
            origin = getattr(template, "origin", None) or getattr(
                template.template, "origin", None
            )
            assert origin is not None
            assert "admin_announcements/contrib/unfold/templates" in origin.name

    def test_banner_present_with_announcement(self, admin_client):
        self._skip_unless_unfold()
        AdminAnnouncement.objects.create(title="Notify", summary="Hello", body="")
        response = admin_client.get("/admin/")
        assert response.status_code == 200
        assert b"announcements-banner" in response.content
        assert b"Notify" in response.content
        assert b"data-announcement-modal" in response.content
        if getattr(settings, "ADMIN_ANNOUNCEMENTS_TESTS_UNFOLD_MODAL", False):
            assert b"unfold_modal/js/modal_core.js" in response.content
        else:
            assert b"unfold_modal/js/modal_core.js" not in response.content
        banner_index = response.content.index(b'id="announcements-banner"')
        content_index = response.content.index(b'id="content"')
        header_index = response.content.index(b'id="header-inner"')
        assert header_index < content_index < banner_index

    def test_banner_absent_from_changelist(self, admin_client):
        self._skip_unless_unfold()
        AdminAnnouncement.objects.create(title="Notify", summary="Hello", body="")
        response = admin_client.get("/admin/admin_announcements/adminannouncement/")
        assert response.status_code == 200
        assert b"announcements-banner" not in response.content

    def test_detail_keeps_unfold_sidebar(self, admin_client):
        self._skip_unless_unfold()
        announcement = AdminAnnouncement.objects.create(
            title="Notify", summary="Hello", body="Body"
        )
        response = admin_client.get(f"/admin/announcements/detail/{announcement.pk}/")
        assert response.status_code == 200
        assert b'id="nav-sidebar"' in response.content

    def test_popup_detail_hides_unfold_sidebar(self, admin_client):
        self._skip_unless_unfold()
        announcement = AdminAnnouncement.objects.create(
            title="Notify", summary="Hello", body="Body"
        )
        response = admin_client.get(
            f"/admin/announcements/detail/{announcement.pk}/?_popup=1"
        )
        assert response.status_code == 200
        assert b'id="nav-sidebar"' not in response.content
        assert response.headers["X-Frame-Options"] == "SAMEORIGIN"

    def test_banner_absent_without_announcement(self, admin_client):
        self._skip_unless_unfold()
        response = admin_client.get("/admin/")
        assert b"announcements-banner" not in response.content


@pytest.mark.django_db
class TestAnnouncementDetailView:
    def test_detail_requires_login(self, client):
        a = AdminAnnouncement.objects.create(title="Secret", summary="", body="Body")
        response = client.get(f"/admin/announcements/detail/{a.pk}/")
        assert response.status_code == 302

    def test_detail_requires_staff(self, client):
        user = User.objects.create_user("u", password="p")
        client.force_login(user)
        a = AdminAnnouncement.objects.create(title="X", summary="Y", body="Z")
        response = client.get(f"/admin/announcements/detail/{a.pk}/")
        assert response.status_code == 302

    def test_detail_404_when_user_not_in_group(self, client):
        group = Group.objects.create(name="editors")
        user = User.objects.create_user("staff", password="p", is_staff=True)
        a = AdminAnnouncement.objects.create(title="Restricted", summary="S", body="B")
        a.groups.add(group)
        client.force_login(user)
        response = client.get(f"/admin/announcements/detail/{a.pk}/")
        assert response.status_code == 404

    def test_detail_renders_when_user_in_group(self, client):
        group = Group.objects.create(name="editors")
        user = User.objects.create_user("staff", password="p", is_staff=True)
        user.groups.add(group)
        a = AdminAnnouncement.objects.create(title="Restricted", summary="S", body="B")
        a.groups.add(group)
        client.force_login(user)
        response = client.get(f"/admin/announcements/detail/{a.pk}/")
        assert response.status_code == 200
        assert b"Restricted" in response.content
