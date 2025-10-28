import csv
import io
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import RequestFactory
from rest_framework.test import APITestCase
from rest_framework import serializers
from mobile_app_version.models import MobileAppVersion
from mobile_app_version.serializers import MobileAppVersionSerializer
from mobile_app_version.validators import validate_semantic_version
from mobile_app_version.admin import MobileAppVersionAdmin


class SemanticVersionValidatorTestCase(TestCase):
    """Test cases for the semantic version validator function."""

    def test_valid_semantic_versions(self):
        """Test that valid semantic version formats are accepted."""
        valid_versions = [
            '0.0.0',
            '0.0.1',
            '0.1.0',
            '1.0.0',
            '1.2.3',
            '10.20.30',
            '100.200.300',
            '999.999.999',
        ]
        
        for version in valid_versions:
            with self.subTest(version=version):
                try:
                    validate_semantic_version(version)
                except ValidationError:
                    self.fail(f"Valid version '{version}' raised ValidationError")

    def test_invalid_semantic_versions(self):
        """Test that invalid semantic version formats are rejected."""
        invalid_versions = [
            # Missing components
            '1',
            '1.0',
            
            # Too many components
            '1.0.0.0',
            '1.0.0.1',
            
            # Non-numeric components
            'a.b.c',
            '1.a.0',
            '1.0.b',
            
            # Leading zeros (not standard semantic versioning)
            '01.0.0',
            '1.01.0',
            '1.0.01',
            
            # Negative numbers
            '-1.0.0',
            '1.-1.0',
            '1.0.-1',
            
            # With prefix/suffix
            'v1.0.0',
            '1.0.0-alpha',
            '1.0.0-beta',
            '1.0.0+build',
            
            # Empty or whitespace
            '',
            ' ',
            '1.0.0 ',
            ' 1.0.0',
            
            # Special characters
            '1.0.0!',
            '1@0@0',
            '1,0,0',
        ]
        
        for version in invalid_versions:
            with self.subTest(version=version):
                with self.assertRaises(ValidationError) as context:
                    validate_semantic_version(version)
                
                # Check that error code is set correctly
                self.assertIn('invalid', context.exception.code)

    def test_non_string_input(self):
        """Test that non-string inputs are rejected."""
        invalid_inputs = [
            123,
            1.0,
            None,
            [],
            {},
        ]
        
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                with self.assertRaises(ValidationError) as context:
                    validate_semantic_version(invalid_input)
                
                self.assertEqual(context.exception.code, 'invalid_type')


class MobileAppVersionModelTestCase(TestCase):
    """Test cases for MobileAppVersion model validation."""

    def test_create_with_valid_version(self):
        """Test creating a MobileAppVersion instance with valid semantic version."""
        valid_versions = ['1.0.0', '2.5.3', '10.0.1']
        
        for version in valid_versions:
            with self.subTest(version=version):
                app_version = MobileAppVersion(
                    version=version,
                    platform_type=MobileAppVersion.PlatformType.ANDROID,
                    link='https://example.com/app.apk'
                )
                # This should not raise ValidationError
                app_version.full_clean()
                app_version.save()
                
                # Verify it was saved correctly
                self.assertEqual(app_version.version, version)
                
                # Clean up
                app_version.delete()

    def test_create_with_invalid_version(self):
        """Test that creating with invalid version raises ValidationError."""
        invalid_versions = ['1.0', 'v1.0.0', '1.0.0-alpha', '1.0.0.0']
        
        for version in invalid_versions:
            with self.subTest(version=version):
                app_version = MobileAppVersion(
                    version=version,
                    platform_type=MobileAppVersion.PlatformType.IOS,
                    link='https://example.com/app.ipa'
                )
                
                with self.assertRaises(ValidationError) as context:
                    app_version.full_clean()
                
                # Check that the error is on the version field
                self.assertIn('version', context.exception.message_dict)

    def test_version_field_attributes(self):
        """Test that version field has correct attributes."""
        version_field = MobileAppVersion._meta.get_field('version')
        
        # Check that validator is attached
        self.assertTrue(any(
            validator.__name__ == 'validate_semantic_version' 
            for validator in version_field.validators
        ))
        
        # Check help text is set
        self.assertIn('semantic versioning', version_field.help_text.lower())


class MobileAppVersionSerializerTestCase(APITestCase):
    """Test cases for MobileAppVersionSerializer validation."""

    def test_serialize_with_valid_version(self):
        """Test serialization with valid semantic versions."""
        valid_data = [
            {
                'version': '1.0.0',
                'platform_type': 'ANDROID',
                'link': 'https://example.com/app.apk',
                'forcing_update': True
            },
            {
                'version': '2.5.10',
                'platform_type': 'IOS',
                'link': 'https://example.com/app.ipa',
                'forcing_update': False
            }
        ]
        
        for data in valid_data:
            with self.subTest(version=data['version']):
                serializer = MobileAppVersionSerializer(data=data)
                self.assertTrue(
                    serializer.is_valid(),
                    msg=f"Serializer errors: {serializer.errors}"
                )

    def test_serialize_with_invalid_version(self):
        """Test that serialization fails with invalid semantic versions."""
        invalid_versions = ['1.0', 'v1.0.0', '1.0.0-beta', 'abc']
        
        for version in invalid_versions:
            with self.subTest(version=version):
                data = {
                    'version': version,
                    'platform_type': 'ANDROID',
                    'link': 'https://example.com/app.apk',
                    'forcing_update': True
                }
                
                serializer = MobileAppVersionSerializer(data=data)
                self.assertFalse(serializer.is_valid())
                self.assertIn('version', serializer.errors)
                
                # Check error message mentions semantic versioning
                error_message = str(serializer.errors['version'][0])
                self.assertIn('semantic versioning', error_message.lower())

    def test_serializer_error_messages(self):
        """Test that serializer provides helpful error messages."""
        data = {
            'version': 'invalid',
            'platform_type': 'ANDROID',
            'link': 'https://example.com/app.apk',
            'forcing_update': True
        }
        
        serializer = MobileAppVersionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        
        # Check that error message includes format example
        error_message = str(serializer.errors['version'][0])
        self.assertIn('X.Y.Z', error_message)

    def test_update_with_different_versions(self):
        """Test updating an existing instance with different version formats."""
        # Create initial instance with valid version
        app_version = MobileAppVersion.objects.create(
            version='1.0.0',
            platform_type=MobileAppVersion.PlatformType.ANDROID,
            link='https://example.com/app.apk'
        )
        
        # Try to update with valid version - should succeed
        serializer = MobileAppVersionSerializer(
            app_version,
            data={
                'version': '2.0.0',
                'platform_type': 'ANDROID',
                'link': 'https://example.com/app.apk',
                'forcing_update': True
            }
        )
        self.assertTrue(serializer.is_valid())
        
        # Try to update with invalid version - should fail
        serializer = MobileAppVersionSerializer(
            app_version,
            data={
                'version': 'invalid',
                'platform_type': 'ANDROID',
                'link': 'https://example.com/app.apk',
                'forcing_update': True
            }
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('version', serializer.errors)
        
        # Clean up
        app_version.delete()


class SemanticVersionEdgeCasesTestCase(TestCase):
    """Test edge cases for semantic versioning."""

    def test_large_version_numbers(self):
        """Test that large version numbers are accepted."""
        large_versions = [
            '999.999.999',
            '1000.0.0',
            '0.1000.0',
            '0.0.1000',
        ]
        
        for version in large_versions:
            with self.subTest(version=version):
                try:
                    validate_semantic_version(version)
                except ValidationError:
                    self.fail(f"Large version '{version}' should be valid")

    def test_zero_versions(self):
        """Test versions with zeros in different positions."""
        zero_versions = [
            '0.0.0',
            '0.0.1',
            '0.1.0',
            '1.0.0',
        ]
        
        for version in zero_versions:
            with self.subTest(version=version):
                try:
                    validate_semantic_version(version)
                except ValidationError:
                    self.fail(f"Zero version '{version}' should be valid")

    def test_version_string_comparison(self):
        """Test that versions are stored as strings, not parsed."""
        app_version = MobileAppVersion.objects.create(
            version='1.0.0',
            platform_type=MobileAppVersion.PlatformType.ANDROID,
            link='https://example.com/app.apk'
        )
        
        # Verify it's stored as string
        self.assertIsInstance(app_version.version, str)
        self.assertEqual(app_version.version, '1.0.0')
        
        app_version.delete()


class MobileAppVersionAdminActionsTestCase(TestCase):
    """Test cases for MobileAppVersion admin bulk actions."""

    def setUp(self):
        """Set up test fixtures."""
        self.site = AdminSite()
        self.admin = MobileAppVersionAdmin(MobileAppVersion, self.site)
        self.factory = RequestFactory()
        
        # Create a superuser for admin requests
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='password123'
        )
        
        # Create test versions
        self.version1 = MobileAppVersion.objects.create(
            version='1.0.0',
            platform_type=MobileAppVersion.PlatformType.ANDROID,
            link='https://example.com/app1.apk',
            forcing_update=False,
            show_update=False,
            release_notes='First version'
        )
        
        self.version2 = MobileAppVersion.objects.create(
            version='2.0.0',
            platform_type=MobileAppVersion.PlatformType.IOS,
            link='https://example.com/app2.ipa',
            forcing_update=True,
            show_update=True,
            release_notes='Second version'
        )
        
        self.version3 = MobileAppVersion.objects.create(
            version='3.0.0',
            platform_type=MobileAppVersion.PlatformType.PWA,
            link='https://example.com/app3/',
            forcing_update=False,
            show_update=False,
            release_notes='Third version'
        )

    def tearDown(self):
        """Clean up test data."""
        MobileAppVersion.objects.all().delete()
        User.objects.all().delete()

    def test_enable_versions_action(self):
        """Test bulk enable versions action."""
        # Select versions that are currently disabled
        queryset = MobileAppVersion.objects.filter(
            id__in=[self.version1.id, self.version3.id]
        )
        
        # Create a mock request
        request = self.factory.post('/admin/mobile_app_version/mobileappversion/')
        request.user = self.user
        
        # Execute the action
        self.admin.enable_versions(request, queryset)
        
        # Verify versions were enabled
        self.version1.refresh_from_db()
        self.version3.refresh_from_db()
        
        self.assertTrue(self.version1.show_update)
        self.assertTrue(self.version3.show_update)
        
        # Verify other version wasn't affected
        self.version2.refresh_from_db()
        self.assertTrue(self.version2.show_update)  # Should remain True

    def test_disable_versions_action(self):
        """Test bulk disable versions action."""
        # Select version that is currently enabled
        queryset = MobileAppVersion.objects.filter(id=self.version2.id)
        
        # Create a mock request
        request = self.factory.post('/admin/mobile_app_version/mobileappversion/')
        request.user = self.user
        
        # Execute the action
        self.admin.disable_versions(request, queryset)
        
        # Verify version was disabled
        self.version2.refresh_from_db()
        self.assertFalse(self.version2.show_update)
        
        # Verify other versions weren't affected
        self.version1.refresh_from_db()
        self.assertFalse(self.version1.show_update)  # Should remain False

    def test_mark_force_update_action(self):
        """Test bulk mark as force update action."""
        # Select versions that don't have force update
        queryset = MobileAppVersion.objects.filter(
            id__in=[self.version1.id, self.version3.id]
        )
        
        # Create a mock request
        request = self.factory.post('/admin/mobile_app_version/mobileappversion/')
        request.user = self.user
        
        # Execute the action
        self.admin.mark_force_update(request, queryset)
        
        # Verify versions were marked for force update
        self.version1.refresh_from_db()
        self.version3.refresh_from_db()
        
        self.assertTrue(self.version1.forcing_update)
        self.assertTrue(self.version3.forcing_update)
        
        # Verify other version wasn't affected
        self.version2.refresh_from_db()
        self.assertTrue(self.version2.forcing_update)  # Should remain True

    def test_unmark_force_update_action(self):
        """Test bulk unmark as force update action."""
        # Select version that has force update enabled
        queryset = MobileAppVersion.objects.filter(id=self.version2.id)
        
        # Create a mock request
        request = self.factory.post('/admin/mobile_app_version/mobileappversion/')
        request.user = self.user
        
        # Execute the action
        self.admin.unmark_force_update(request, queryset)
        
        # Verify version was unmarked from force update
        self.version2.refresh_from_db()
        self.assertFalse(self.version2.forcing_update)
        
        # Verify other versions weren't affected
        self.version1.refresh_from_db()
        self.assertFalse(self.version1.forcing_update)  # Should remain False

    def test_export_to_csv_action(self):
        """Test CSV export action."""
        # Select all versions
        queryset = MobileAppVersion.objects.all().order_by('id')
        
        # Create a mock request
        request = self.factory.post('/admin/mobile_app_version/mobileappversion/')
        request.user = self.user
        
        # Execute the action
        response = self.admin.export_to_csv(request, queryset)
        
        # Verify response is a CSV file
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename="mobile_app_versions.csv"'
        )
        
        # Parse CSV content
        content = response.content.decode('utf-8')
        csv_reader = csv.reader(io.StringIO(content))
        rows = list(csv_reader)
        
        # Verify header
        expected_header = [
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
        ]
        self.assertEqual(rows[0], expected_header)
        
        # Verify data rows (should have 3 versions + 1 header)
        self.assertEqual(len(rows), 4)
        
        # Verify first data row
        self.assertEqual(rows[1][1], '1.0.0')  # Version
        self.assertEqual(rows[1][2], 'ANDROID')  # Platform Type
        self.assertEqual(rows[1][3], 'First version')  # Release Notes
        self.assertEqual(rows[1][6], 'False')  # Forcing Update
        self.assertEqual(rows[1][7], 'False')  # Show Update

    def test_export_to_csv_with_selected_versions(self):
        """Test CSV export with only selected versions."""
        # Select only two versions
        queryset = MobileAppVersion.objects.filter(
            id__in=[self.version1.id, self.version2.id]
        ).order_by('id')
        
        # Create a mock request
        request = self.factory.post('/admin/mobile_app_version/mobileappversion/')
        request.user = self.user
        
        # Execute the action
        response = self.admin.export_to_csv(request, queryset)
        
        # Parse CSV content
        content = response.content.decode('utf-8')
        csv_reader = csv.reader(io.StringIO(content))
        rows = list(csv_reader)
        
        # Verify only 2 versions were exported (+ 1 header)
        self.assertEqual(len(rows), 3)
        
        # Verify the correct versions were exported
        versions_in_csv = [rows[1][1], rows[2][1]]
        self.assertIn('1.0.0', versions_in_csv)
        self.assertIn('2.0.0', versions_in_csv)
        self.assertNotIn('3.0.0', versions_in_csv)

    def test_admin_actions_are_registered(self):
        """Test that all actions are properly registered in admin."""
        actions = self.admin.get_actions(None)
        
        # Verify all custom actions are registered
        self.assertIn('enable_versions', actions)
        self.assertIn('disable_versions', actions)
        self.assertIn('mark_force_update', actions)
        self.assertIn('unmark_force_update', actions)
        self.assertIn('export_to_csv', actions)

    def test_enable_all_versions(self):
        """Test enabling all versions at once."""
        # All versions start with various states
        queryset = MobileAppVersion.objects.all()
        
        # Create a mock request
        request = self.factory.post('/admin/mobile_app_version/mobileappversion/')
        request.user = self.user
        
        # Execute the action
        self.admin.enable_versions(request, queryset)
        
        # Verify all versions are now enabled
        for version in MobileAppVersion.objects.all():
            self.assertTrue(
                version.show_update,
                f"Version {version.version} should be enabled"
            )

    def test_mark_all_force_update(self):
        """Test marking all versions for force update at once."""
        # All versions start with various states
        queryset = MobileAppVersion.objects.all()
        
        # Create a mock request
        request = self.factory.post('/admin/mobile_app_version/mobileappversion/')
        request.user = self.user
        
        # Execute the action
        self.admin.mark_force_update(request, queryset)
        
        # Verify all versions are now marked for force update
        for version in MobileAppVersion.objects.all():
            self.assertTrue(
                version.forcing_update,
                f"Version {version.version} should be marked for force update"
            )
