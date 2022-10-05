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

    def get(self, request):
        app_versions = MobileAppVersion.objects.order_by('-created_at').all()
        paginator = PageNumberSizedPagination()
        try:
            app_versions = paginator.paginate_queryset(app_versions, request)
        except NotFound as e:
            return Response({
                'success': False,
                'messages': e.detail,
            }, status=status.HTTP_400_BAD_REQUEST)

        app_serializer = MobileAppVersionSerializer(app_versions, many=True)
        paginated_result = paginator.get_paginated_response(app_serializer.data)
        return Response({
            'success': True,
            'data': paginated_result.data
        })

    def post(self, request):
        app_serializer = MobileAppVersionSerializer(data=request.data)
        if not app_serializer.is_valid():
            return Response({
                'success': False,
                'errors': app_serializer.error_messages
            }, status=status.HTTP_400_BAD_REQUEST)
        app_serializer.save()
        return Response({
            'success': True,
            'data': app_serializer.data
        }, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        app_versions = MobileAppVersion.objects.filter(pk=pk)
        if not app_versions.exists():
            return Response({
                'success': False,
                'messages': DATA_NOT_FOUND_MESSAGE,
            }, status=status.HTTP_400_BAD_REQUEST)
        app_version = app_versions.first()
        app_serializer = MobileAppVersionSerializer(app_version, data=request.data, partial=True)
        if not app_serializer.is_valid():
            return Response({
                'success': False,
                'errors': app_serializer.error_messages
            }, status=status.HTTP_400_BAD_REQUEST)
        app_serializer.save()
        return Response({
            'success': True,
            'data': app_serializer.data
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        app_versions = MobileAppVersion.objects.filter(pk=pk)
        if not app_versions.exists():
            return Response({
                'success': False,
                'messages': DATA_NOT_FOUND_MESSAGE,
            }, status=status.HTTP_400_BAD_REQUEST)
        app_vers = app_versions.first()
        app_vers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
