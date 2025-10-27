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

1. Add `'mobile_app_version.apps.MobileAppVersionConfig'` and `'drf_spectacular'` to your `INSTALLED_APPS` in _`settings.py`_ module:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'drf_spectacular',
    'mobile_app_version.apps.MobileAppVersionConfig',
]
```

2. Configure drf-spectacular in your `settings.py`:
```python
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Mobile App Version API',
    'DESCRIPTION': 'API for managing mobile app versions across Android, iOS, and PWA platforms',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': r'/api',
}
```

3. Include the Mobile App Version URLconf in your projects `urls.py` like this:
```python
from django.urls import path, include

urlpatterns = [
    ...
    # API endpoints
    path('api/app-versions/', include('mobile_app_version.urls')),
    path('api/admin/app-versions/', include('mobile_app_version.adminapi.urls')),
    
    # API Documentation (optional but recommended)
    path('api/docs/', include('mobile_app_version.docs_urls')),
]
```

4. Run migrations to create the database tables:
```sh
python manage.py migrate mobile_app_version
```

If you clone this app directly in your project and have changes to application models, first run:
```sh
python manage.py makemigrations mobile_app_version
python manage.py migrate mobile_app_version
```

## API Documentation

This package includes comprehensive API documentation using **drf-spectacular** with both Swagger UI and ReDoc interfaces.

### Accessing Documentation

After including the documentation URLs (step 3 above), you can access:

- **Swagger UI**: `http://localhost:8000/api/docs/swagger/`  
  Interactive API documentation with "Try it out" functionality
  
- **ReDoc**: `http://localhost:8000/api/docs/redoc/`  
  Beautiful, responsive API documentation
  
- **OpenAPI Schema**: `http://localhost:8000/api/docs/schema/`  
  Raw OpenAPI 3.0 schema (JSON format)

### Documentation Features

- 📝 Detailed endpoint descriptions
- 📊 Request/response examples for all endpoints
- 🔐 Authentication requirements clearly marked
- ✅ Field validation rules and formats
- 🎯 Interactive API testing (Swagger UI)
- 📱 Separate documentation for Public and Admin APIs

## API Endpoints

### Public API

These endpoints are publicly accessible without authentication:

- `GET /api/app-versions/latest?type={ANDROID|IOS|PWA}` - Get latest version by platform type
- `GET /api/app-versions/info/{android|ios|pwa}` - Get latest version info by platform

### Admin API

These endpoints require authentication and admin permissions:

- `GET /api/admin/app-versions/apps` - List all app versions (paginated)
- `POST /api/admin/app-versions/apps` - Create a new app version
- `PUT /api/admin/app-versions/apps/{id}` - Update an app version
- `DELETE /api/admin/app-versions/apps/{id}` - Delete an app version

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
