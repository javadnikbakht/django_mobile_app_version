from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from mobile_app_version.models import MobileAppVersion
from mobile_app_version.serializers import MobileAppVersionSerializer


@permission_classes((AllowAny,))
class AppInfoView(APIView):
    """
    Retrieve the latest version information for a specific mobile app platform.
    
    This endpoint returns the most recent app version details for the specified
    platform type (Android, iOS, or PWA). It includes version number, download link,
    release notes, and update requirements.
    """
    
    @extend_schema(
        summary="Get latest app info by platform",
        description=(
            "Returns the latest mobile app version information for the specified platform type. "
            "This endpoint is typically used by mobile apps on launch to check if an update "
            "is available and whether it should be forced."
        ),
        parameters=[
            OpenApiParameter(
                name="platform_type",
                type=str,
                location=OpenApiParameter.PATH,
                description="Platform type: android, ios, or pwa",
                enum=["android", "ios", "pwa"],
                required=True,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=MobileAppVersionSerializer,
                description="Successfully retrieved app information",
                examples=[
                    OpenApiExample(
                        "Android App Version",
                        value={
                            "success": True,
                            "data": {
                                "app": {
                                    "id": 1,
                                    "version": "1.2.3",
                                    "platform_type": "ANDROID",
                                    "release_notes": "Bug fixes and performance improvements",
                                    "link": "https://example.com/app-v1.2.3.apk",
                                    "link_32": "https://example.com/app-v1.2.3-32bit.apk",
                                    "forcing_update": True,
                                    "manifest": None,
                                    "show_update": True,
                                    "created_at": "2025-01-15T10:30:00Z",
                                }
                            },
                        },
                        response_only=True,
                    ),
                    OpenApiExample(
                        "iOS App Version",
                        value={
                            "success": True,
                            "data": {
                                "app": {
                                    "id": 2,
                                    "version": "2.0.0",
                                    "platform_type": "IOS",
                                    "release_notes": "Major update with new features",
                                    "link": "https://apps.apple.com/app/myapp/id123456789",
                                    "link_32": None,
                                    "forcing_update": False,
                                    "manifest": None,
                                    "show_update": True,
                                    "created_at": "2025-01-20T14:20:00Z",
                                }
                            },
                        },
                        response_only=True,
                    ),
                ],
            ),
        },
        tags=["Public API"],
    )
    def get(self, request, platform_type):
        app = (
            MobileAppVersion.objects.filter(platform_type=platform_type)
            .order_by("-id")
            .first()
        )
        app_serializer = MobileAppVersionSerializer(app)

        return Response(
            {
                "success": True,
                "data": {
                    "app": app_serializer.data,
                },
            },
            status=status.HTTP_200_OK,
        )


@permission_classes((AllowAny,))
class LatestAppVersion(APIView):
    """
    Retrieve the latest app version by platform type using query parameters.
    
    This endpoint provides the same functionality as the app info endpoint but
    accepts the platform type as a query parameter instead of a path parameter.
    """
    
    @extend_schema(
        summary="Get latest app version",
        description=(
            "Returns the latest app version for the platform type specified in the query parameter. "
            "Useful for checking version updates dynamically."
        ),
        parameters=[
            OpenApiParameter(
                name="type",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Platform type (ANDROID, IOS, or PWA)",
                required=True,
                examples=[
                    OpenApiExample(
                        "Android",
                        value="ANDROID",
                    ),
                    OpenApiExample(
                        "iOS",
                        value="IOS",
                    ),
                    OpenApiExample(
                        "PWA",
                        value="PWA",
                    ),
                ],
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=MobileAppVersionSerializer,
                description="Successfully retrieved the latest app version",
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={
                            "success": True,
                            "data": {
                                "id": 5,
                                "version": "3.1.0",
                                "platform_type": "ANDROID",
                                "release_notes": "New features:\n- Dark mode support\n- Improved performance\n- Bug fixes",
                                "link": "https://example.com/downloads/app-v3.1.0.apk",
                                "link_32": "https://example.com/downloads/app-v3.1.0-32bit.apk",
                                "forcing_update": False,
                                "manifest": None,
                                "show_update": True,
                                "created_at": "2025-01-27T09:15:00Z",
                            },
                        },
                        response_only=True,
                    ),
                ],
            ),
        },
        tags=["Public API"],
    )
    def get(self, request):
        app = MobileAppVersion.objects.filter(
            platform_type=request.GET.get("type", "")
        ).last()
        app_serializer = MobileAppVersionSerializer(app)
        return Response(
            {
                "success": True,
                "data": app_serializer.data,
            }
        )
