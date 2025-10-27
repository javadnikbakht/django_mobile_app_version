from rest_framework import serializers

from mobile_app_version.models import MobileAppVersion
from mobile_app_version.validators import validate_semantic_version


class MobileAppVersionSerializer(serializers.ModelSerializer):
    """
    Serializer for Mobile App Version model.
    
    Handles validation and serialization of mobile app version information
    including version number, platform type, download links, and update settings.
    """
    
    id = serializers.IntegerField(
        read_only=True,
        help_text="Unique identifier for the app version"
    )
    
    version = serializers.CharField(
        max_length=100,
        validators=[validate_semantic_version],
        help_text="Version must follow semantic versioning format (X.Y.Z). Example: 1.0.0, 2.3.4"
    )
    
    platform_type = serializers.ChoiceField(
        choices=MobileAppVersion.PlatformType.choices,
        help_text="Platform type: ANDROID, IOS, or PWA"
    )
    
    release_notes = serializers.CharField(
        required=False,
        allow_blank=True,
        style={'base_template': 'textarea.html'},
        help_text="Release notes describing what's new in this version"
    )
    
    link = serializers.URLField(
        max_length=255,
        help_text="Download link or app store URL for the app"
    )
    
    link_32 = serializers.URLField(
        max_length=255,
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text="Optional download link for 32-bit version (Android only)"
    )
    
    forcing_update = serializers.BooleanField(
        default=True,
        help_text="Whether users must update to this version to continue using the app"
    )
    
    manifest = serializers.URLField(
        max_length=255,
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text="URL to the PWA manifest file (PWA only)"
    )
    
    show_update = serializers.BooleanField(
        default=False,
        help_text="Whether to show update notification to users"
    )
    
    created_at = serializers.DateTimeField(
        read_only=True,
        help_text="Timestamp when this version was created"
    )
    
    class Meta:
        model = MobileAppVersion
        fields = "__all__"
