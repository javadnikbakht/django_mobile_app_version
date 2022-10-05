from django.contrib import admin

from mobile_app_version.models import MobileAppVersion


@admin.register(MobileAppVersion)
class MobileAppVersionAdmin(admin.ModelAdmin):
    list_display = (
        'version',
        'platform_type',
        'manifest',
        'forcing_update',
        'created_at',
        'show_update',
    )
    list_editable = (
        'forcing_update',
        'show_update',
    )
    list_filter = ['created_at', "forcing_update", "show_update"]
    search_fields = ['version', 'platform_type']
