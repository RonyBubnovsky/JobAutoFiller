"""URL and field validation utilities."""

import re

# URL validation pattern for Comeet job links
COMEET_URL_PATTERN = re.compile(r'^https?://(www\.)?comeet\.com/jobs/.+', re.IGNORECASE)


def is_valid_comeet_url(url: str) -> bool:
    """Check if URL is a valid Comeet job link.
    
    Args:
        url: The URL string to validate.
        
    Returns:
        True if the URL is a valid Comeet job link, False otherwise.
    """
    return bool(COMEET_URL_PATTERN.match(url.strip()))


def validate_required_fields(form_data: dict, required_fields: list) -> list:
    """Check that all required fields are filled.
    
    Args:
        form_data: Dictionary of field names to StringVar objects.
        required_fields: List of field names that are required.
        
    Returns:
        List of missing field names.
    """
    missing_fields = []
    for field_name in required_fields:
        if field_name in form_data:
            value = form_data[field_name].get().strip()
            if not value:
                missing_fields.append(field_name)
    return missing_fields
