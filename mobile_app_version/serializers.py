from rest_framework import serializers

from mobile_app_version.models import MobileAppVersion


class MobileAppVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileAppVersion
        fields = '__all__'
