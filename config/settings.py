"""Configuration for Alexandria"""

# Database settings
DATABASE_LOCATION = "data"

# Logging settings
LOGGING_LEVEL = "INFO"
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Default settings
DEFAULT_AUTHOR = "Unknown"
DEFAULT_PREVIEW_LENGTH = 200

# UI Settings
COLORS = {
    "success": "\033[92m",  # Green
    "error": "\033[91m",    # Red
    "warning": "\033[93m",  # Yellow
    "info": "\033[94m",     # Blue
    "reset": "\033[0m",     # Reset
}

# Feature flags
FEATURES = {
    "enable_encryption": False,
    "enable_api": False,
    "enable_sync": False,
}
