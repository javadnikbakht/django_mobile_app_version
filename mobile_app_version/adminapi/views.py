from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from mobile_app_version.adminapi.permissions import IsAppVersioningMember
from mobile_app_version.messages import DATA_NOT_FOUND_MESSAGE
from mobile_app_version.models import MobileAppVersion
from mobile_app_version.paginations import PageNumberSizedPagination
from mobile_app_version.serializers import MobileAppVersionSerializer


@permission_classes((IsAuthenticated, IsAppVersioningMember))
class AppVersioningAdminView(APIView):
    """
    Admin endpoints for managing mobile app versions.
    
    Provides CRUD operations for app version management. Requires authentication
    and app versioning member permissions.
    """
    
    @extend_schema(
        summary="List all app versions",
        description=(
            "Retrieves a paginated list of all mobile app versions, ordered by creation date (newest first). "
            "Supports pagination through query parameters."
        ),
        parameters=[
            OpenApiParameter(
                name="page",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Page number for pagination",
                required=False,
            ),
            OpenApiParameter(
                name="page_size",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Number of items per page",
                required=False,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=MobileAppVersionSerializer(many=True),
                description="Successfully retrieved app versions",
                examples=[
                    OpenApiExample(
                        "Paginated Response",
                        value={
                            "success": True,
                            "data": {
                                "count": 25,
                                "next": "http://api.example.com/admin/apps?page=2",
                                "previous": None,
                                "results": [
                                    {
                                        "id": 10,
                                        "version": "2.5.0",
                                        "platform_type": "ANDROID",
                                        "release_notes": "Performance improvements and bug fixes",
                                        "link": "https://example.com/app-v2.5.0.apk",
                                        "link_32": "https://example.com/app-v2.5.0-32bit.apk",
                                        "forcing_update": False,
                                        "manifest": None,
                                        "show_update": True,
                                        "created_at": "2025-01-27T10:00:00Z",
                                    },
                                    {
                                        "id": 9,
                                        "version": "1.8.0",
                                        "platform_type": "IOS",
                                        "release_notes": "New features and enhancements",
                                        "link": "https://apps.apple.com/app/myapp/id123456789",
                                        "link_32": None,
                                        "forcing_update": True,
                                        "manifest": None,
                                        "show_update": True,
                                        "created_at": "2025-01-26T15:30:00Z",
                                    },
                                ],
                            },
                        },
                        response_only=True,
                    ),
                ],
            ),
            400: OpenApiResponse(
                description="Bad request - invalid pagination parameters",
                examples=[
                    OpenApiExample(
                        "Pagination Error",
                        value={
                            "success": False,
                            "messages": "Invalid page.",
                        },
                    ),
                ],
            ),
        },
        tags=["Admin API"],
    )
    def get(self, request):
        app_versions = MobileAppVersion.objects.order_by("-created_at").all()
        paginator = PageNumberSizedPagination()
        try:
            app_versions = paginator.paginate_queryset(app_versions, request)
        except NotFound as e:
            return Response(
                {
                    "success": False,
                    "messages": e.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        app_serializer = MobileAppVersionSerializer(app_versions, many=True)
        paginated_result = paginator.get_paginated_response(app_serializer.data)
        return Response({"success": True, "data": paginated_result.data})

    @extend_schema(
        summary="Create a new app version",
        description=(
            "Creates a new mobile app version entry. The version must follow semantic versioning "
            "format (X.Y.Z). All required fields must be provided."
        ),
        request=MobileAppVersionSerializer,
        responses={
            201: OpenApiResponse(
                response=MobileAppVersionSerializer,
                description="App version created successfully",
                examples=[
                    OpenApiExample(
                        "Created Android Version",
                        value={
                            "success": True,
                            "data": {
                                "id": 15,
                                "version": "3.0.0",
                                "platform_type": "ANDROID",
                                "release_notes": "Major release with exciting new features:\n- New UI design\n- Enhanced security\n- Better performance",
                                "link": "https://example.com/app-v3.0.0.apk",
                                "link_32": "https://example.com/app-v3.0.0-32bit.apk",
                                "forcing_update": True,
                                "manifest": None,
                                "show_update": True,
                                "created_at": "2025-01-27T12:00:00Z",
                            },
                        },
                        response_only=True,
                    ),
                ],
            ),
            400: OpenApiResponse(
                description="Bad request - validation errors",
                examples=[
                    OpenApiExample(
                        "Validation Error",
                        value={
                            "success": False,
                            "errors": {
                                "version": [
                                    "Version must follow semantic versioning format (X.Y.Z). Each component must be a non-negative integer. Example: 1.0.0, 2.3.4"
                                ],
                                "link": ["This field is required."],
                            },
                        },
                    ),
                ],
            ),
        },
        examples=[
            OpenApiExample(
                "Create Android Version",
                value={
                    "version": "2.1.0",
                    "platform_type": "ANDROID",
                    "release_notes": "Bug fixes and improvements",
                    "link": "https://example.com/app-v2.1.0.apk",
                    "link_32": "https://example.com/app-v2.1.0-32bit.apk",
                    "forcing_update": False,
                    "show_update": True,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Create iOS Version",
                value={
                    "version": "1.5.2",
                    "platform_type": "IOS",
                    "release_notes": "Minor update with stability improvements",
                    "link": "https://apps.apple.com/app/myapp/id123456789",
                    "forcing_update": False,
                    "show_update": True,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Create PWA Version",
                value={
                    "version": "1.0.0",
                    "platform_type": "PWA",
                    "release_notes": "Initial PWA release",
                    "link": "https://example.com/pwa",
                    "manifest": "https://example.com/manifest.json",
                    "forcing_update": False,
                    "show_update": True,
                },
                request_only=True,
            ),
        ],
        tags=["Admin API"],
    )
    def post(self, request):
        app_serializer = MobileAppVersionSerializer(data=request.data)
        if not app_serializer.is_valid():
            return Response(
                {"success": False, "errors": app_serializer.error_messages},
                status=status.HTTP_400_BAD_REQUEST,
            )
        app_serializer.save()
        return Response(
            {"success": True, "data": app_serializer.data},
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Update an app version",
        description=(
            "Updates an existing mobile app version. Supports partial updates - "
            "only provided fields will be updated. The version format must still "
            "follow semantic versioning if provided."
        ),
        parameters=[
            OpenApiParameter(
                name="pk",
                type=int,
                location=OpenApiParameter.PATH,
                description="The ID of the app version to update",
                required=True,
            ),
        ],
        request=MobileAppVersionSerializer,
        responses={
            200: OpenApiResponse(
                response=MobileAppVersionSerializer,
                description="App version updated successfully",
                examples=[
                    OpenApiExample(
                        "Updated Version",
                        value={
                            "success": True,
                            "data": {
                                "id": 5,
                                "version": "2.1.1",
                                "platform_type": "ANDROID",
                                "release_notes": "Updated release notes with additional information",
                                "link": "https://example.com/app-v2.1.1.apk",
                                "link_32": "https://example.com/app-v2.1.1-32bit.apk",
                                "forcing_update": True,
                                "manifest": None,
                                "show_update": True,
                                "created_at": "2025-01-20T10:00:00Z",
                            },
                        },
                        response_only=True,
                    ),
                ],
            ),
            400: OpenApiResponse(
                description="Bad request - version not found or validation error",
                examples=[
                    OpenApiExample(
                        "Not Found",
                        value={
                            "success": False,
                            "messages": "Data not found",
                        },
                    ),
                    OpenApiExample(
                        "Validation Error",
                        value={
                            "success": False,
                            "errors": {
                                "version": [
                                    "Version must follow semantic versioning format (X.Y.Z)."
                                ]
                            },
                        },
                    ),
                ],
            ),
        },
        examples=[
            OpenApiExample(
                "Partial Update - Change forcing_update",
                value={
                    "forcing_update": True,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Partial Update - Update release notes",
                value={
                    "release_notes": "Updated: Critical security fixes included",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Full Update",
                value={
                    "version": "2.2.0",
                    "platform_type": "ANDROID",
                    "release_notes": "Completely updated release",
                    "link": "https://example.com/app-v2.2.0.apk",
                    "forcing_update": False,
                    "show_update": True,
                },
                request_only=True,
            ),
        ],
        tags=["Admin API"],
    )
    def put(self, request, pk):
        app_versions = MobileAppVersion.objects.filter(pk=pk)
        if not app_versions.exists():
            return Response(
                {
                    "success": False,
                    "messages": DATA_NOT_FOUND_MESSAGE,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        app_version = app_versions.first()
        app_serializer = MobileAppVersionSerializer(
            app_version, data=request.data, partial=True
        )
        if not app_serializer.is_valid():
            return Response(
                {"success": False, "errors": app_serializer.error_messages},
                status=status.HTTP_400_BAD_REQUEST,
            )
        app_serializer.save()
        return Response(
            {"success": True, "data": app_serializer.data}, status=status.HTTP_200_OK
        )

    @extend_schema(
        summary="Delete an app version",
        description=(
            "Permanently deletes a mobile app version from the database. "
            "This action cannot be undone."
        ),
        parameters=[
            OpenApiParameter(
                name="pk",
                type=int,
                location=OpenApiParameter.PATH,
                description="The ID of the app version to delete",
                required=True,
            ),
        ],
        responses={
            204: OpenApiResponse(
                description="App version deleted successfully (no content returned)",
            ),
            400: OpenApiResponse(
                description="Bad request - version not found",
                examples=[
                    OpenApiExample(
                        "Not Found",
                        value={
                            "success": False,
                            "messages": "Data not found",
                        },
                    ),
                ],
            ),
        },
        tags=["Admin API"],
    )
    def delete(self, request, pk):
        app_versions = MobileAppVersion.objects.filter(pk=pk)
        if not app_versions.exists():
            return Response(
                {
                    "success": False,
                    "messages": DATA_NOT_FOUND_MESSAGE,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        app_vers = app_versions.first()
        app_vers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
