# django-mobile-app-version

## Quick start

1. Install the package
```sh
pip install django-mobile-app-version
```

2. Add `'mobile_app_version.apps.MobileAppVersionConfig'` to your `INSTALLED_APPS` in _`settings.py`_ module:
```python3
INSTALLED_APPS = [
    ...
    'mobile_app_version.apps.MobileAppVersionConfig',
]
```

3. Include the Mobile App Version URLconf in your projects `urls.py` like this:
```
path('app-versions', include('mobile_app_version')),
```

4. Run `python manage.py migrate mobile_app_version` to create the tables of app in your database. if you clone this app
directly in your project and have some changes on application models you should first run 
`pyhton manage.py makemigrations mobile_app_version` and then migrate models.
