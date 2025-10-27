"""
URL configuration for API documentation.

Include these URLs in your project's urls.py to enable interactive API documentation:

    from django.urls import path, include
    
    urlpatterns = [
        ...
        path('api/docs/', include('mobile_app_version.docs_urls')),
    ]

This provides:
- /api/docs/schema/ - OpenAPI 3.0 schema (JSON/YAML)
- /api/docs/swagger/ - Swagger UI interface
- /api/docs/redoc/ - ReDoc interface
"""

from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # OpenAPI 3.0 schema
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    
    # Swagger UI
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    
    # ReDoc UI
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

