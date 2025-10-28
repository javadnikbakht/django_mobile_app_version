import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from mobile_app_version.models import MobileAppVersion


@admin.register(MobileAppVersion)
class MobileAppVersionAdmin(admin.ModelAdmin):
    list_display = (
        "version",
        "platform_type",
        "manifest",
        "forcing_update",
        "created_at",
        "show_update",
    )
    list_editable = (
        "forcing_update",
        "show_update",
    )
    list_filter = ["created_at", "forcing_update", "show_update"]
    search_fields = ["version", "platform_type"]
    actions = [
        "enable_versions",
        "disable_versions",
        "mark_force_update",
        "unmark_force_update",
        "export_to_csv",
    ]

    @admin.action(description=_("Enable selected versions"))
    def enable_versions(self, request, queryset):
        """Bulk enable versions by setting show_update to True."""
        updated = queryset.update(show_update=True)
        self.message_user(
            request,
            _(f"{updated} version(s) successfully enabled."),
        )

    @admin.action(description=_("Disable selected versions"))
    def disable_versions(self, request, queryset):
        """Bulk disable versions by setting show_update to False."""
        updated = queryset.update(show_update=False)
        self.message_user(
            request,
            _(f"{updated} version(s) successfully disabled."),
        )

    @admin.action(description=_("Mark as force update"))
    def mark_force_update(self, request, queryset):
        """Bulk mark versions as requiring force update."""
        updated = queryset.update(forcing_update=True)
        self.message_user(
            request,
            _(f"{updated} version(s) marked as force update."),
        )

    @admin.action(description=_("Unmark as force update"))
    def unmark_force_update(self, request, queryset):
        """Bulk unmark versions from requiring force update."""
        updated = queryset.update(forcing_update=False)
        self.message_user(
            request,
            _(f"{updated} version(s) unmarked as force update."),
        )

    @admin.action(description=_("Export selected to CSV"))
    def export_to_csv(self, request, queryset):
        """Export selected versions to CSV file."""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="mobile_app_versions.csv"'
        
        writer = csv.writer(response)
        # Write header
        writer.writerow([
            "ID",
            "Version",
            "Platform Type",
            "Release Notes",
            "Link",
            "Link 32",
            "Forcing Update",
            "Show Update",
            "Manifest",
            "Created At",
        ])
        
        # Write data rows
        for version in queryset:
            writer.writerow([
                version.id,
                version.version,
                version.platform_type,
                version.release_notes,
                version.link,
                version.link_32,
                version.forcing_update,
                version.show_update,
                version.manifest,
                version.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            ])
        
        self.message_user(
            request,
            _(f"{queryset.count()} version(s) exported to CSV."),
        )
        
        return response
