# django-admin-announcements

Admin announcements for Django, with optional [django-unfold](https://github.com/unfoldadmin/django-unfold) layout integration.

> **Status:** Testing. No package released yet.

## Features

- Displays a list of active announcements above the Django admin header as a banner.
- Allows admins to create announcements in the standard Django admin for editors (`is_staff`)
- Announcements can be assigned to groups and are time- and date-sensitive
- Allows editors to dismiss active announcements (stored in local storage)
- Support optional markdown content if installed with `markdown` support (only for rendered HTML, no special fields)
- Supports [django-unfold](https://github.com/unfoldadmin/django-unfold) using an optional `contrib.unfold` app
- Supports [django-unfold-modal](https://github.com/metaforx/django-unfold-modal) to display announcements in a modal instead of a full page
- Customize implementation via template tag `admin_announcements_banner`

## Requirements

- Python 3.10+
- Django 5.0+
- (Optional) django-unfold 0.52.0+ for the `contrib.unfold` integration

## Markdown support
- If installed with `markdown` support, announcements can contain markdown and will be rendered as HTML.
- [nh3](https://github.com/messense/nh3) is used to sanitize HTML and prevent XSS.
- [concrete.css](https://github.com/louismerlin/concrete.css) (3kb) is used for markdown styling.

## Installation

```bash
pip install django-admin-announcements
```

Install with markdown rendering support:

```bash
pip install "django-admin-announcements[markdown]"
```

Install with both markdown and Unfold support:

```bash
pip install "django-admin-announcements[markdown,unfold]"
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
    "admin_announcements.contrib.unfold",
    "unfold",
    "unfold_modal",  # Optional: enables modal announcement detail links.
    "admin_announcements",
    "django.contrib.admin",
    # ...
]
```

Keep `admin_announcements.contrib.unfold` before `unfold` so its Unfold-aware
admin template override is discovered first.

To open announcement detail links in an Unfold modal, also install the
`unfold-modal` extra and load `django-unfold-modal` assets in your Unfold
settings:

```bash
uv sync --extra unfold --extra unfold-modal --group test --group dev
```

```python
from unfold_modal.utils import get_modal_scripts, get_modal_styles

UNFOLD = {
    # ...
    "STYLES": [*get_modal_styles()],
    "SCRIPTS": [*get_modal_scripts()],
}
```

Without `django-unfold-modal` scripts, the links fall back to normal detail pages.

Run migrations:

```bash
python manage.py migrate admin_announcements
```

## Local Development

Install dependencies:

```bash
uv sync --group test --group dev
npm ci
```

Install pre-commit hooks:

```bash
uv run pre-commit install
```

Run all pre-commit hooks manually:

```bash
uv run pre-commit run --all-files
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
