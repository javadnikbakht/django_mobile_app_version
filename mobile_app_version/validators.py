import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_semantic_version(value):
    """
    Validates that a version string follows semantic versioning format (X.Y.Z).
    
    Semantic versioning format: MAJOR.MINOR.PATCH
    - MAJOR: Incremented for incompatible API changes
    - MINOR: Incremented for backwards-compatible functionality additions
    - PATCH: Incremented for backwards-compatible bug fixes
    
    Examples of valid versions:
        - 1.0.0
        - 0.1.0
        - 1.2.3
        - 10.20.30
    
    Examples of invalid versions:
        - 1.0
        - v1.0.0
        - 1.0.0-alpha
        - 1.0.0.1
    
    Args:
        value (str): The version string to validate
        
    Raises:
        ValidationError: If the version string doesn't match the semantic versioning format
    """
    # Regular expression for semantic versioning (MAJOR.MINOR.PATCH)
    # Each component must be a non-negative integer
    semantic_version_pattern = r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$'
    
    if not isinstance(value, str):
        raise ValidationError(
            _('Version must be a string.'),
            code='invalid_type'
        )
    
    if not re.match(semantic_version_pattern, value):
        raise ValidationError(
            _(
                'Version must follow semantic versioning format (X.Y.Z). '
                'Each component must be a non-negative integer. '
                'Example: 1.0.0, 2.3.4'
            ),
            code='invalid_semantic_version',
            params={'value': value}
        )

