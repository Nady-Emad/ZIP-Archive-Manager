# ZIP Archive Manager API Documentation

## Overview

The ZIP Archive Manager provides a comprehensive API for working with ZIP archives through modular utility classes.

## Core Modules

### utils.zip_manager

The main module for ZIP archive operations.

#### ZIPManager

Main class for managing ZIP archive operations.

**Constructor:**
```python
ZIPManager(progress_callback: Optional[Callable] = None)
```

**Methods:**

##### create_archive()
```python
create_archive(
    archive_path: str,
    files: List[str],
    compression_method: int = zipfile.ZIP_DEFLATED,
    password: Optional[str] = None,
    base_dir: Optional[str] = None
) -> bool
```
Create a ZIP archive from files/directories.

**Parameters:**
- `archive_path`: Path where the ZIP file will be created
- `files`: List of file/directory paths to add to archive
- `compression_method`: Compression method constant (ZIP_STORED, ZIP_DEFLATED, ZIP_BZIP2, ZIP_LZMA)
- `password`: Optional password for encryption
- `base_dir`: Base directory for relative paths

**Returns:** `True` if successful, `False` otherwise

**Example:**
```python
from utils.zip_manager import ZIPManager
from utils.compression import CompressionHandler, CompressionMethod

manager = ZIPManager()
success = manager.create_archive(
    archive_path='output.zip',
    files=['file1.txt', 'folder/'],
    compression_method=CompressionHandler.get_compression_value(CompressionMethod.LZMA),
    password='secret123'
)
```

##### extract_archive()
```python
extract_archive(
    archive_path: str,
    extract_path: str,
    password: Optional[str] = None,
    members: Optional[List[str]] = None
) -> bool
```
Extract a ZIP archive.

**Parameters:**
- `archive_path`: Path to the ZIP file
- `extract_path`: Directory where files will be extracted
- `password`: Optional password for encrypted archives
- `members`: Optional list of specific members to extract

**Returns:** `True` if successful, `False` otherwise

**Example:**
```python
manager = ZIPManager()
success = manager.extract_archive(
    archive_path='archive.zip',
    extract_path='output/',
    password='secret123'
)
```

##### list_contents()
```python
list_contents(
    archive_path: str,
    password: Optional[str] = None
) -> Optional[List[dict]]
```
List contents of a ZIP archive.

**Returns:** List of dictionaries containing file information:
- `filename`: Name of the file
- `compressed_size`: Compressed size in bytes
- `uncompressed_size`: Uncompressed size in bytes
- `compression_type`: Compression type constant
- `date_time`: Date/time tuple
- `is_dir`: Whether item is a directory
- `crc`: CRC checksum

**Example:**
```python
manager = ZIPManager()
contents = manager.list_contents('archive.zip')
for item in contents:
    print(f"{item['filename']}: {item['uncompressed_size']} bytes")
```

##### get_archive_info()
```python
get_archive_info(archive_path: str) -> Optional[dict]
```
Get detailed information about a ZIP archive.

**Returns:** Dictionary with:
- `path`: Archive path
- `file_count`: Number of files
- `total_compressed_size`: Total compressed size
- `total_uncompressed_size`: Total uncompressed size
- `compression_ratio`: Compression ratio percentage
- `archive_size`: Archive file size

### utils.compression

Module for handling compression methods.

#### CompressionMethod

Enumeration of supported compression methods:
- `STORE`: No compression
- `DEFLATE`: Standard ZIP compression
- `BZIP2`: BZIP2 compression
- `LZMA`: LZMA compression

#### CompressionHandler

Handles compression method selection and information.

**Class Methods:**

##### get_compression_value()
```python
get_compression_value(method: CompressionMethod) -> int
```
Get the zipfile compression constant.

##### get_compression_name()
```python
get_compression_name(method: CompressionMethod) -> str
```
Get the display name for a compression method.

##### get_compression_info()
```python
get_compression_info(method: CompressionMethod) -> Dict[str, str]
```
Get detailed information about a compression method.

**Returns:** Dictionary with `name`, `description`, `speed`, `ratio`, `cpu_usage`.

##### from_string()
```python
from_string(method_str: str) -> CompressionMethod
```
Convert string to CompressionMethod enum.

**Example:**
```python
from utils.compression import CompressionHandler, CompressionMethod

# Get compression value
method = CompressionMethod.LZMA
value = CompressionHandler.get_compression_value(method)

# Get information
info = CompressionHandler.get_compression_info(method)
print(info['description'])

# Convert from string
method = CompressionHandler.from_string('lzma')
```

### utils.security

Module for password protection and encryption.

#### SecurityManager

Manages security features for ZIP archives.

**Class Methods:**

##### validate_password()
```python
validate_password(password: str) -> tuple[bool, str]
```
Validate password strength.

**Returns:** Tuple of (is_valid, message)

##### generate_password()
```python
generate_password(length: int = 16, include_special: bool = True) -> str
```
Generate a secure random password.

##### test_archive_password()
```python
test_archive_password(archive_path: str, password: str) -> bool
```
Test if a password is correct for an encrypted archive.

##### is_encrypted()
```python
is_encrypted(archive_path: str) -> bool
```
Check if a ZIP archive is password-protected.

**Example:**
```python
from utils.security import SecurityManager

# Validate password
is_valid, msg = SecurityManager.validate_password('mypassword')
if not is_valid:
    print(f"Invalid: {msg}")

# Generate secure password
password = SecurityManager.generate_password(length=20)

# Check if archive is encrypted
if SecurityManager.is_encrypted('archive.zip'):
    print("Archive is password protected")
```

### utils.validators

Module for archive validation and verification.

#### ArchiveValidator

Validates and verifies ZIP archive integrity.

**Static Methods:**

##### validate_archive()
```python
validate_archive(archive_path: str) -> tuple[bool, str]
```
Validate ZIP archive integrity.

**Returns:** Tuple of (is_valid, message)

##### verify_crc()
```python
verify_crc(archive_path: str) -> Dict[str, any]
```
Verify CRC checksums for all files in archive.

**Returns:** Dictionary with verification results including:
- `valid`: Overall validity
- `total_files`: Total number of files
- `verified_files`: Successfully verified files
- `failed_files`: List of failed files
- `errors`: List of errors

##### get_archive_stats()
```python
get_archive_stats(archive_path: str) -> Optional[Dict]
```
Get detailed statistics about archive.

**Example:**
```python
from utils.validators import ArchiveValidator

# Validate archive
is_valid, msg = ArchiveValidator.validate_archive('archive.zip')
print(f"Valid: {is_valid}, Message: {msg}")

# Verify CRC
results = ArchiveValidator.verify_crc('archive.zip')
print(f"Verified {results['verified_files']} files")

# Get statistics
stats = ArchiveValidator.get_archive_stats('archive.zip')
print(f"Total files: {stats['total_files']}")
```

### utils.batch_operations

Module for batch processing of multiple archives.

#### BatchProcessor

Handles batch operations on multiple archives.

**Constructor:**
```python
BatchProcessor(progress_callback: Optional[Callable] = None)
```

**Methods:**

##### batch_create()
```python
batch_create(
    operations: List[Dict],
    compression_method: int,
    password: Optional[str] = None
) -> Dict[str, any]
```
Create multiple ZIP archives in batch.

**Parameters:**
- `operations`: List of dicts with `archive_path` and `files` keys
- `compression_method`: Compression method to use
- `password`: Optional password for all archives

**Returns:** Results dictionary with `total`, `successful`, `failed`, `errors`.

##### batch_extract()
```python
batch_extract(
    operations: List[Dict],
    password: Optional[str] = None
) -> Dict[str, any]
```
Extract multiple ZIP archives in batch.

**Parameters:**
- `operations`: List of dicts with `archive_path` and `extract_path` keys
- `password`: Optional password for encrypted archives

##### batch_verify()
```python
batch_verify(archive_paths: List[str]) -> Dict[str, any]
```
Verify multiple ZIP archives in batch.

**Example:**
```python
from utils.batch_operations import BatchProcessor

processor = BatchProcessor()

# Batch extract
operations = [
    {'archive_path': 'archive1.zip', 'extract_path': 'output1/'},
    {'archive_path': 'archive2.zip', 'extract_path': 'output2/'}
]
results = processor.batch_extract(operations)
print(f"Extracted {results['successful']} archives")
```

### utils.progress_tracker

Module for tracking operation progress.

#### ProgressTracker

Tracks and reports progress of operations.

**Constructor:**
```python
ProgressTracker(callback: Optional[Callable] = None)
```

**Methods:**

##### start()
```python
start(total: int, message: str = "Starting...")
```
Start tracking progress.

##### update()
```python
update(current: int, message: str = "")
```
Update progress.

##### complete()
```python
complete(message: str = "Complete")
```
Mark operation as complete.

##### error()
```python
error(message: str)
```
Report an error.

#### ConsoleProgressTracker

Progress tracker that prints to console with formatted output and progress bars.

**Example:**
```python
from utils.progress_tracker import ConsoleProgressTracker

tracker = ConsoleProgressTracker()
tracker.start(100, "Processing files...")

for i in range(100):
    # Do work
    tracker.update(i + 1, f"Processing file {i + 1}")

tracker.complete("All files processed")
```

## Progress Callbacks

All main operations support progress callbacks with signature:
```python
def callback(current: int, total: int, message: str):
    """
    current: Current progress value
    total: Total number of items
    message: Status message
    """
    pass
```

**Example:**
```python
def my_callback(current, total, message):
    percentage = (current / total) * 100 if total > 0 else 0
    print(f"[{percentage:.1f}%] {message}")

manager = ZIPManager(my_callback)
manager.create_archive('output.zip', ['files/'])
```

## Error Handling

All operations return success/failure indicators and provide error messages through progress trackers. Always check return values:

```python
manager = ZIPManager()
success = manager.create_archive('output.zip', ['files/'])

if not success:
    print("Archive creation failed")
else:
    print("Archive created successfully")
```

## Thread Safety

The utility modules are designed to be used in single-threaded contexts. For GUI applications, use Qt's threading mechanisms (QThread) to run operations in background threads.

## Complete Example

```python
from utils.zip_manager import ZIPManager
from utils.compression import CompressionMethod, CompressionHandler
from utils.security import SecurityManager
from utils.validators import ArchiveValidator
from utils.progress_tracker import ConsoleProgressTracker

# Create with progress tracking
tracker = ConsoleProgressTracker()
manager = ZIPManager(tracker._console_callback)

# Validate password
password = "secure123"
is_valid, msg = SecurityManager.validate_password(password)
if not is_valid:
    print(f"Password invalid: {msg}")
    exit(1)

# Create archive
success = manager.create_archive(
    archive_path='myarchive.zip',
    files=['data/'],
    compression_method=CompressionHandler.get_compression_value(CompressionMethod.LZMA),
    password=password
)

if success:
    # Verify the archive
    is_valid, msg = ArchiveValidator.validate_archive('myarchive.zip')
    print(f"Archive valid: {is_valid}")
    
    # Get archive info
    info = manager.get_archive_info('myarchive.zip')
    print(f"Files: {info['file_count']}")
    print(f"Compression ratio: {info['compression_ratio']:.1f}%")
```
