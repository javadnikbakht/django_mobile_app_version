from rest_framework import serializers

from mobile_app_version.models import MobileAppVersion
from mobile_app_version.validators import validate_semantic_version


class MobileAppVersionSerializer(serializers.ModelSerializer):
    version = serializers.CharField(
        max_length=100,
        validators=[validate_semantic_version],
        help_text='Version must follow semantic versioning format (X.Y.Z). Example: 1.0.0'
    )
    
    class Meta:
        model = MobileAppVersion
        fields = "__all__"
