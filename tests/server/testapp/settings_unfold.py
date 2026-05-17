from .settings import *  # noqa: F403

INSTALLED_APPS = [
    "admin_announcements.contrib.unfold",
    "unfold",
    "unfold.contrib.filters",
    "admin_announcements",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "testapp",
]

UNFOLD = {}

ADMIN_ANNOUNCEMENTS_TESTS_UNFOLD = True
