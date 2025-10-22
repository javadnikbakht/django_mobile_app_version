from django.db import models

from mobile_app_version.validators import validate_semantic_version


class MobileAppVersion(models.Model):
    class PlatformType(models.TextChoices):
        ANDROID = "ANDROID", "android"
        IOS = "IOS", "ios"
        PWA = "PWA", "pwa"

    version = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        validators=[validate_semantic_version],
        help_text='Version must follow semantic versioning format (X.Y.Z). Example: 1.0.0'
    )
    platform_type = models.CharField(
        max_length=10, choices=PlatformType.choices, null=False, blank=False
    )
    release_notes = models.TextField(blank=True)
    link = models.URLField(max_length=255, null=False, blank=False)
    link_32 = models.URLField(max_length=255, null=True, blank=True)
    forcing_update = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    manifest = models.URLField(max_length=255, null=True, blank=True)
    show_update = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Mobile App Version"
        verbose_name_plural = "Mobile App Version"

    def __str__(self):
        return f"App <{self.platform_type}, {self.version}>"
