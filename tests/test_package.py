"""Tests for admin_announcements package metadata."""


class TestPackageImport:
    """Verify package can be imported and has expected attributes."""

    def test_import_package(self):
        import admin_announcements

        assert admin_announcements.__version__ == "0.1.0a0"

    def test_import_app_config(self):
        from admin_announcements.apps import AdminAnnouncementsConfig

        assert AdminAnnouncementsConfig.name == "admin_announcements"

    def test_import_unfold_contrib_app_config(self):
        from admin_announcements.contrib.unfold.apps import (
            AdminAnnouncementsUnfoldConfig,
        )

        assert (
            AdminAnnouncementsUnfoldConfig.name
            == "admin_announcements.contrib.unfold"
        )
        assert (
            AdminAnnouncementsUnfoldConfig.label == "admin_announcements_unfold"
        )
