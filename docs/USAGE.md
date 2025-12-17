# ZIP Archive Manager - Detailed Usage Guide

## Table of Contents
- [Installation](#installation)
- [GUI Application Usage](#gui-application-usage)
- [CLI Application Usage](#cli-application-usage)
- [Common Use Cases](#common-use-cases)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
# Navigate to project directory
cd ZIP-Archive-Manager

# Install required packages
pip install -r requirements.txt
```

### Verify Installation

```bash
# Test CLI
python zip_manager_cli.py --help

# Test GUI (requires display)
python zip_manager_gui.py
```

## GUI Application Usage

### Launching the GUI

```bash
python zip_manager_gui.py
```

### Tab 1: Create Archive

**Step-by-Step:**

1. **Add Files/Folders**:
   - Click "Add Files" to select individual files
   - Click "Add Folder" to select entire directories
   - Multiple selections are supported
   - Review selected items in the list

2. **Select Compression Method**:
   - **Store**: No compression, fastest (for already compressed files)
   - **Deflate**: Standard compression (recommended for most cases)
   - **BZIP2**: Better compression (good for text files)
   - **LZMA**: Best compression (slowest, best for archival)

3. **Password Protection** (Optional):
   - Check "Password Protection" box
   - Enter a secure password (minimum 4 characters)
   - Password strength warnings will be shown

4. **Select Output Location**:
   - Click "Browse" next to "Output File"
   - Choose location and name for your ZIP file
   - .zip extension added automatically

5. **Create Archive**:
   - Click "Create Archive" button
   - Progress bar shows creation progress
   - Success message appears when complete

### Tab 2: Extract Archive

**Step-by-Step:**

1. **Select Archive**:
   - Click "Browse" next to "Archive File"
   - Select the ZIP file to extract

2. **Choose Destination**:
   - Click "Browse" next to "Extract To"
   - Select or create destination folder

3. **Enter Password** (if encrypted):
   - Enter password in the password field
   - Leave empty if archive is not encrypted

4. **Extract**:
   - Click "Extract Archive" button
   - Progress bar shows extraction progress
   - Files will be extracted to chosen location

### Tab 3: View Archive

**Step-by-Step:**

1. **Select Archive**:
   - Click "Browse" to select a ZIP file
   - Click "View Contents"

2. **Review Information**:
   - Top section shows archive statistics
   - Table shows detailed file listing with:
     - File names
     - Original sizes
     - Compressed sizes
     - Compression ratios
     - Compression types

3. **Verify Integrity**:
   - Click "Verify Archive Integrity"
   - Results show if archive is valid
   - CRC checksums are verified

### Tab 4: Batch Operations

**Batch Extract:**

1. Click "Add Archives" to select multiple ZIP files
2. Review list of archives
3. Click "Batch Extract"
4. Select destination folder
5. Each archive extracts to its own subfolder
6. Results summary shows in text area

**Batch Verify:**

1. Click "Add Archives" to select multiple ZIP files
2. Click "Batch Verify"
3. All archives are validated
4. Results show valid/invalid counts

## CLI Application Usage

### General Syntax

```bash
python zip_manager_cli.py <command> [arguments] [options]
```

### Command Reference

#### 1. Create Archive

**Basic Usage:**
```bash
python zip_manager_cli.py create OUTPUT.zip FILE1 [FILE2 ...] [OPTIONS]
```

**Options:**
- `-c, --compression`: Compression method (store, deflate, bzip2, lzma)
- `-p, --password`: Password for encryption
- `-b, --base-dir`: Base directory for relative paths

**Examples:**

```bash
# Create archive with default compression
python zip_manager_cli.py create backup.zip documents/

# Create with LZMA compression
python zip_manager_cli.py create backup.zip documents/ -c lzma

# Create with password
python zip_manager_cli.py create secure.zip secrets/ -p mypassword

# Create with specific files
python zip_manager_cli.py create files.zip file1.txt file2.txt file3.txt

# Combine options
python zip_manager_cli.py create archive.zip data/ -c bzip2 -p secret123
```

#### 2. Extract Archive

**Basic Usage:**
```bash
python zip_manager_cli.py extract ARCHIVE.zip -o OUTPUT_DIR [OPTIONS]
```

**Options:**
- `-o, --output`: Output directory (required)
- `-p, --password`: Password for encrypted archive
- `-m, --members`: Specific files to extract

**Examples:**

```bash
# Extract entire archive
python zip_manager_cli.py extract backup.zip -o restored/

# Extract with password
python zip_manager_cli.py extract secure.zip -o data/ -p mypassword

# Extract specific files
python zip_manager_cli.py extract archive.zip -o output/ -m file1.txt file2.txt

# Extract to current directory
python zip_manager_cli.py extract archive.zip -o ./
```

#### 3. List Contents

**Basic Usage:**
```bash
python zip_manager_cli.py list ARCHIVE.zip [OPTIONS]
```

**Options:**
- `-d, --detailed`: Show detailed information
- `-p, --password`: Password for encrypted archive

**Examples:**

```bash
# Simple listing
python zip_manager_cli.py list archive.zip

# Detailed listing with sizes
python zip_manager_cli.py list archive.zip -d

# List encrypted archive
python zip_manager_cli.py list secure.zip -p mypassword
```

#### 4. Verify Archive

**Basic Usage:**
```bash
python zip_manager_cli.py verify ARCHIVE.zip [OPTIONS]
```

**Options:**
- `--crc`: Verify CRC checksums

**Examples:**

```bash
# Basic verification
python zip_manager_cli.py verify archive.zip

# Full CRC verification
python zip_manager_cli.py verify archive.zip --crc
```

#### 5. Archive Information

**Basic Usage:**
```bash
python zip_manager_cli.py info ARCHIVE.zip
```

**Example:**

```bash
python zip_manager_cli.py info backup.zip
```

Output includes:
- Archive size
- Total files
- Compression statistics
- Encryption status
- File type breakdown

#### 6. Batch Extract

**Basic Usage:**
```bash
python zip_manager_cli.py batch-extract ARCHIVE1.zip [ARCHIVE2.zip ...] -o OUTPUT_DIR [OPTIONS]
```

**Options:**
- `-o, --output`: Output directory (required)
- `-p, --password`: Password for encrypted archives

**Examples:**

```bash
# Extract multiple archives
python zip_manager_cli.py batch-extract arch1.zip arch2.zip arch3.zip -o extracted/

# With password
python zip_manager_cli.py batch-extract *.zip -o output/ -p password123
```

#### 7. Batch Verify

**Basic Usage:**
```bash
python zip_manager_cli.py batch-verify ARCHIVE1.zip [ARCHIVE2.zip ...]
```

**Example:**

```bash
# Verify multiple archives
python zip_manager_cli.py batch-verify archive1.zip archive2.zip archive3.zip

# Verify all ZIP files in directory
python zip_manager_cli.py batch-verify *.zip
```

## Common Use Cases

### Use Case 1: Backup Important Files

**GUI:**
1. Open GUI → "Create Archive" tab
2. Add your important folders
3. Select LZMA compression for best space saving
4. Enable password protection
5. Choose backup location (e.g., external drive)
6. Click "Create Archive"

**CLI:**
```bash
python zip_manager_cli.py create backup_$(date +%Y%m%d).zip ~/Documents ~/Pictures -c lzma -p BackupPass123
```

### Use Case 2: Send Files via Email

**GUI:**
1. Open GUI → "Create Archive" tab
2. Add files to send
3. Use Deflate compression (good balance)
4. Don't use password (unless recipient knows it)
5. Save to Desktop or Downloads
6. Attach created ZIP to email

**CLI:**
```bash
python zip_manager_cli.py create email_files.zip file1.pdf file2.docx presentation.pptx -c deflate
```

### Use Case 3: Extract Downloaded Archives

**GUI:**
1. Open GUI → "Extract Archive" tab
2. Browse and select downloaded ZIP
3. Choose destination folder
4. Click "Extract Archive"

**CLI:**
```bash
python zip_manager_cli.py extract downloaded_file.zip -o ~/Downloads/extracted/
```

### Use Case 4: Verify Archive Integrity

**Before important operations, verify archives:**

**GUI:**
1. Open GUI → "View Archive" tab
2. Select archive
3. Click "Verify Archive Integrity"

**CLI:**
```bash
python zip_manager_cli.py verify important_archive.zip --crc
```

### Use Case 5: Batch Process Multiple Archives

**Extract many archives at once:**

**GUI:**
1. Open GUI → "Batch Operations" tab
2. Click "Add Archives" and select all ZIPs
3. Click "Batch Extract"
4. Choose destination folder
5. Each archive extracts to its own folder

**CLI:**
```bash
python zip_manager_cli.py batch-extract *.zip -o extracted_archives/
```

## Advanced Features

### Password Security

**Strong Password Guidelines:**
- Minimum 4 characters (12+ recommended)
- Mix uppercase and lowercase
- Include numbers
- Include special characters

**Generate Secure Password (Python API):**
```python
from utils.security import SecurityManager
password = SecurityManager.generate_password(length=16)
print(password)
```

### Compression Method Selection Guide

**When to use each method:**

| Method | Use When |
|--------|----------|
| Store | Files are already compressed (JPG, PNG, MP4, etc.) |
| Deflate | General purpose, need speed and decent compression |
| BZIP2 | Text files, source code, need better compression |
| LZMA | Maximum compression needed, time is not critical |

### Progress Tracking

**GUI:** 
- Automatic progress bars
- Status messages in status bar

**CLI:**
- Console progress bars
- Real-time status messages
- Operation timing

### Relative vs Absolute Paths

**Absolute paths in archive** (default):
```bash
# Creates: /home/user/documents/file.txt in archive
python zip_manager_cli.py create archive.zip /home/user/documents/file.txt
```

**Relative paths using base-dir**:
```bash
# Creates: file.txt in archive
python zip_manager_cli.py create archive.zip /home/user/documents/file.txt -b /home/user/documents/
```

## Troubleshooting

### Issue: "Password incorrect" error

**Solutions:**
- Verify password is correct
- Check for extra spaces
- Ensure correct case (passwords are case-sensitive)
- Test password:
```python
from utils.security import SecurityManager
result = SecurityManager.test_archive_password('archive.zip', 'password')
print(result)  # True if correct
```

### Issue: Archive appears corrupted

**Solutions:**
1. Verify archive:
```bash
python zip_manager_cli.py verify archive.zip --crc
```

2. Check if file transfer was complete
3. Try re-downloading/re-creating the archive

### Issue: Extraction fails

**Common causes:**
- Insufficient disk space
- No write permissions
- Files already exist (may need to delete)
- Archive is corrupted

**Solutions:**
- Free up disk space
- Choose different destination
- Check permissions
- Verify archive integrity first

### Issue: GUI doesn't start

**Solutions:**
1. Check PyQt5 installation:
```bash
pip install --upgrade PyQt5
```

2. Verify Python version:
```bash
python --version  # Should be 3.7+
```

3. Check display availability (for headless systems)

### Issue: Slow compression

**Expected for:**
- BZIP2 and LZMA methods
- Large files
- Many small files

**Solutions:**
- Use Deflate for faster compression
- Use Store for already compressed files
- Process files in smaller batches

### Issue: Cannot add large files

**ZIP format limits:**
- Standard ZIP: 4 GB file limit
- ZIP64 (automatic): No practical limit

**Note:** Python's zipfile module automatically uses ZIP64 when needed.

## Tips and Best Practices

1. **Always verify important archives** after creation
2. **Use appropriate compression** for your file types
3. **Keep passwords secure** and backed up separately
4. **Test extraction** before deleting originals
5. **Use batch operations** for multiple files to save time
6. **Check available disk space** before large operations
7. **Use relative paths** in archives for portability
8. **Regular backups** using password-protected LZMA archives

## Getting Help

### Command Help

```bash
# General help
python zip_manager_cli.py --help

# Command-specific help
python zip_manager_cli.py create --help
python zip_manager_cli.py extract --help
```

### GUI Help

- Click "Help" → "About" in the menu bar
- Tooltips appear on hover (where available)

### Documentation

- Check `README.md` for overview
- Check `docs/API.md` for programmatic usage
- Check this file (`docs/USAGE.md`) for detailed usage

### Support

- Report issues on GitHub
- Check existing issues for solutions
- Include error messages and steps to reproduce
