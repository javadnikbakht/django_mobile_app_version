from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from mobile_app_version.models import MobileAppVersion
from mobile_app_version.serializers import MobileAppVersionSerializer


@permission_classes((AllowAny,))
class AppInfoView(APIView):

    def get(self, request, platform_type):
        app = MobileAppVersion.objects.filter(platform_type=platform_type).order_by('-id').first()
        app_serializer = MobileAppVersionSerializer(app)

        return Response({
            'success': True,
            'data': {
                'app': app_serializer.data,
            },
        }, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class LatestAppVersion(APIView):

    def get(self, request):
        app = MobileAppVersion.objects.filter(
            platform_type=request.GET.get('type', '')).last()
        app_serializer = MobileAppVersionSerializer(app)
        return Response({
            'success': True,
            'data': app_serializer.data,
        })
