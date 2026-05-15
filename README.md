# django-admin-announcements

Admin announcements and notifications for Django, with optional [django-unfold](https://github.com/unfoldadmin/django-unfold) layout integration.

> **Status:** Draft / early scaffold. Models are not stable.

## Features (planned)

- `AdminAnnouncement` model for time-bounded admin notices
- Pluggable layout via `admin_announcements.contrib.unfold` for Unfold admin UI
- Display full announcement content using a modal [django-unfold-modal(https://github.com/metaforx/django-unfold-modal)]
- Minimal core that works with stock Django admin

## Requirements

- Python 3.10+
- Django 5.0+
- (Optional) django-unfold 0.52.0+ for the `contrib.unfold` integration

## Installation

```bash
pip install django-admin-announcements
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "admin_announcements",
    "django.contrib.admin",
    # ...
]
```

For Unfold integration, also add the contrib app:

```python
INSTALLED_APPS = [
    "unfold",
    "admin_announcements",
    "admin_announcements.contrib.unfold",
    "django.contrib.admin",
    # ...
]
```

Run migrations:

```bash
python manage.py migrate admin_announcements
```

## Local Development

Install dependencies:

```bash
uv sync --group test --group dev
```

Run the stock Django test server:

```bash
uv run tests/server/manage.py runserver 8080
```

Run the Unfold test server:

```bash
uv run --extra unfold tests/server/manage.py runserver 8080 --settings=testapp.settings_unfold
```

## License

MIT
