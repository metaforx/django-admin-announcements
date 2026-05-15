"""Smoke tests to verify test infrastructure is working."""

from datetime import timedelta

import pytest
from django.conf import settings
from django.contrib.admin.sites import site as admin_site
from django.contrib.auth.models import Group
from django.utils import timezone

from admin_announcements.models import AdminAnnouncement


@pytest.mark.django_db
class TestAdminAnnouncementModel:
    """Verify AdminAnnouncement is properly defined and can be persisted."""

    def test_create_minimal(self):
        announcement = AdminAnnouncement.objects.create(
            version="1.0.0",
            title="Welcome",
            summary="Initial release",
            body="The system is now live.",
            starts_at=timezone.now(),
        )
        assert announcement.pk is not None
        assert announcement.is_active is True
        assert announcement.expires_at is None

    def test_str_representation(self):
        announcement = AdminAnnouncement(version="2.0.0", title="Update")
        assert str(announcement) == "2.0.0 — Update"

    def test_ordering_is_most_recent_first(self):
        now = timezone.now()
        older = AdminAnnouncement.objects.create(
            version="1.0.0",
            title="Old",
            summary="",
            body="",
            starts_at=now - timedelta(days=2),
        )
        newer = AdminAnnouncement.objects.create(
            version="1.1.0",
            title="New",
            summary="",
            body="",
            starts_at=now,
        )
        assert list(AdminAnnouncement.objects.all()) == [newer, older]


@pytest.mark.django_db
class TestAdminAnnouncementGroups:
    """Group assignment is optional — none, one, or many."""

    def _make_announcement(self):
        return AdminAnnouncement.objects.create(
            version="1.0.0",
            title="t",
            summary="",
            body="",
            starts_at=timezone.now(),
        )

    def test_no_groups_assigned(self):
        a = self._make_announcement()
        assert a.groups.count() == 0

    def test_single_group_assigned(self):
        group = Group.objects.create(name="editors")
        a = self._make_announcement()
        a.groups.add(group)
        assert list(a.groups.all()) == [group]

    def test_multiple_groups_assigned(self):
        g1 = Group.objects.create(name="g1")
        g2 = Group.objects.create(name="g2")
        a = self._make_announcement()
        a.groups.add(g1, g2)
        assert a.groups.count() == 2

    def test_reverse_relation_from_group(self):
        group = Group.objects.create(name="editors")
        a = self._make_announcement()
        a.groups.add(group)
        assert list(group.admin_announcements.all()) == [a]


class TestAdminRegistration:
    """Verify the model is registered with the admin site."""

    def test_admin_announcement_registered(self):
        registered = {model.__name__ for model in admin_site._registry}
        assert "AdminAnnouncement" in registered

    def test_unfold_contrib_replaces_default_admin(self):
        """contrib.unfold should re-register AdminAnnouncement with an
        unfold.admin.ModelAdmin-derived admin class."""
        if not getattr(settings, "ADMIN_ANNOUNCEMENTS_TESTS_UNFOLD", False):
            pytest.skip("Unfold integration is tested with testapp.settings_unfold")

        from unfold.admin import ModelAdmin as UnfoldModelAdmin

        admin_obj = admin_site._registry[AdminAnnouncement]
        assert isinstance(admin_obj, UnfoldModelAdmin)


@pytest.mark.django_db
class TestAdminAccess:
    """Verify admin pages for AdminAnnouncement are accessible."""

    def test_admin_index(self, admin_client):
        response = admin_client.get("/admin/")
        assert response.status_code == 200

    def test_announcement_changelist(self, admin_client):
        response = admin_client.get("/admin/admin_announcements/adminannouncement/")
        assert response.status_code == 200

    def test_announcement_add(self, admin_client):
        response = admin_client.get(
            "/admin/admin_announcements/adminannouncement/add/"
        )
        assert response.status_code == 200
