from django.utils.deprecation import MiddlewareMixin
from packaging.version import parse as parse_version
from rest_framework import status
from rest_framework.response import Response

from mobile_app_version.messages import REQUIRED_HEADERS_NOT_SENT
from mobile_app_version.messages import UNSUPPORTED_PLATFORM_MESSAGE
from mobile_app_version.messages import UPGRADE_TO_LATEST_VERSION_MESSAGE
from mobile_app_version.models import MobileAppVersion
from mobile_app_version.serializers import MobileAppVersionSerializer


class AppVersionControlMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith("/admin/"):
            return
        app_platform = request.headers.get("App-Platform", "").lower()
        app_version = request.headers.get("App-Version", "")
        supported_platforms = MobileAppVersion.PlatformType.values
        if not (app_platform and app_version):
            return Response(data={
                "success": False,
                "message": REQUIRED_HEADERS_NOT_SENT
            }, status=status.HTTP_400_BAD_REQUEST)

        if app_platform not in supported_platforms:
            return Response(data={
                "success": False,
                "message": UNSUPPORTED_PLATFORM_MESSAGE,
            }, status=status.HTTP_400_BAD_REQUEST)

        last_force_update_version = MobileAppVersion.objects.filter(platform_type=app_platform,
                                                                    forcing_update=True).last().version
        if parse_version(app_version) < parse_version(last_force_update_version):
            latest_app_version = MobileAppVersion.objects.filter(type=app_platform).last()
            if latest_app_version:
                app_serializer = MobileAppVersionSerializer(latest_app_version)
                return Response(data={
                    "success": False,
                    "message": UPGRADE_TO_LATEST_VERSION_MESSAGE,
                    "data": {
                        "force-update-to": app_serializer.data,
                    },
                }, status=420)
