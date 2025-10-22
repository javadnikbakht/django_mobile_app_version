# django-mobile-app-version

A Django app for managing mobile app versions through your API.

## Requirements

- Python 3.13+
- Django 3.0+
- Django REST Framework 3.14+

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

## Version Format

### Semantic Versioning

The `version` field follows [Semantic Versioning](https://semver.org/) format: **X.Y.Z**

- **X** (Major): Incremented for incompatible API changes
- **Y** (Minor): Incremented for backwards-compatible functionality additions  
- **Z** (Patch): Incremented for backwards-compatible bug fixes

#### Valid Version Examples
```
1.0.0
2.5.3
10.20.30
0.1.0
```

#### Invalid Version Examples
```
1.0          # Missing patch version
v1.0.0       # Prefix not allowed
1.0.0-alpha  # Pre-release tags not allowed
1.0.0.1      # Too many components
01.0.0       # Leading zeros not allowed
```

### API Usage

When creating or updating a mobile app version through the API, the version field must follow the semantic versioning format:

```python
# Valid request
{
    "version": "1.0.0",
    "platform_type": "ANDROID",
    "link": "https://example.com/app.apk",
    "forcing_update": true
}

# Invalid request - will return validation error
{
    "version": "v1.0.0",  # Error: Version must follow semantic versioning format (X.Y.Z)
    "platform_type": "ANDROID",
    "link": "https://example.com/app.apk"
}
```

### Error Messages

If an invalid version format is provided, you'll receive a clear error message:

```json
{
    "version": [
        "Version must follow semantic versioning format (X.Y.Z). Each component must be a non-negative integer. Example: 1.0.0, 2.3.4"
    ]
}
```

## Contributing

Interested in contributing? Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for development setup instructions and guidelines.
