from .settings import *  # noqa: F403

try:
    from unfold_modal.utils import get_modal_scripts, get_modal_styles
except ImportError:
    get_modal_scripts = None
    get_modal_styles = None

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

ADMIN_ANNOUNCEMENTS_TESTS_UNFOLD_MODAL = get_modal_scripts is not None

if ADMIN_ANNOUNCEMENTS_TESTS_UNFOLD_MODAL:
    INSTALLED_APPS.insert(3, "unfold_modal")
    UNFOLD = {
        "STYLES": [*get_modal_styles()],
        "SCRIPTS": [*get_modal_scripts()],
    }
else:
    UNFOLD = {}

ADMIN_ANNOUNCEMENTS_TESTS_UNFOLD = True
