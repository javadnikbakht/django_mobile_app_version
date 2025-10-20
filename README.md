# django-mobile-app-version

A Django app for managing mobile app versions through your API.

## Installation

```sh
pip install django-mobile-app-version
```

## Quick Start

1. Add `'mobile_app_version.apps.MobileAppVersionConfig'` to your `INSTALLED_APPS` in _`settings.py`_ module:
```python
INSTALLED_APPS = [
    ...
    'mobile_app_version.apps.MobileAppVersionConfig',
]
```

2. Include the Mobile App Version URLconf in your projects `urls.py` like this:
```python
path('app-versions', include('mobile_app_version')),
```

3. Run migrations to create the database tables:
```sh
python manage.py migrate mobile_app_version
```

If you clone this app directly in your project and have changes to application models, first run:
```sh
python manage.py makemigrations mobile_app_version
python manage.py migrate mobile_app_version
```

## Contributing

Interested in contributing? Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for development setup instructions and guidelines.
