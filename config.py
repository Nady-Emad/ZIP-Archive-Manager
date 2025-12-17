"""
Application Configuration
"""

import os

# Application metadata
APP_NAME = "ZIP Archive Manager"
APP_VERSION = "3.2.0"
APP_AUTHOR = "ZIP Archive Manager Team"

# Default settings
DEFAULT_COMPRESSION = "deflate"
DEFAULT_PASSWORD_LENGTH = 16

# File size limits (in bytes)
MAX_FILE_SIZE = 4 * 1024 * 1024 * 1024  # 4 GB (ZIP64 limit)
WARNING_FILE_SIZE = 1 * 1024 * 1024 * 1024  # 1 GB

# Supported file extensions
ARCHIVE_EXTENSIONS = ['.zip']

# Compression methods
COMPRESSION_METHODS = {
    'store': 0,      # No compression
    'deflate': 8,    # Standard ZIP compression
    'bzip2': 12,     # BZIP2 compression
    'lzma': 14       # LZMA compression
}

# UI Settings
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# Progress update frequency (in items)
PROGRESS_UPDATE_INTERVAL = 10

# Batch operation settings
MAX_BATCH_SIZE = 100
BATCH_TIMEOUT = 3600  # 1 hour in seconds
