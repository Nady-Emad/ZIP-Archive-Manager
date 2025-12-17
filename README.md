# ZIP Archive Manager v3.2

A powerful and feature-rich ZIP archive management tool built with Python. Designed for users who need advanced compression, extraction, and archive manipulation capabilities with both GUI and command-line interfaces.

## Features

### Core Functionality
- **Archive Creation**: Create ZIP files from single or multiple files/folders
- **Archive Extraction**: Extract files with optional password protection support
- **Batch Operations**: Process multiple archives simultaneously
- **Compression Options**: Multiple compression levels (Store, Deflate, Bzip2, LZMA)
- **Password Protection**: Create and extract password-protected archives
- **Archive Inspection**: View file structure, size information, and compression ratios

### User Interfaces
- **Graphical User Interface (GUI)**: Intuitive PyQt5-based interface for easy interaction
- **Command-Line Interface (CLI)**: Powerful command-line tools for automation and scripting
- **Drag & Drop Support**: Simple drag-and-drop functionality for quick operations

### Advanced Features
- File preview and metadata viewing
- Selective extraction of specific files
- Archive verification and integrity checking
- Compression statistics and analysis
- Memory-efficient handling of large files
- Cross-platform compatibility (Windows, Linux, macOS)

## Quick Start

### Option 1: Windows Executable (Recommended)
**No installation required!**

1. Download `ZIP-Archive-Manager-v3.2.exe`
2. Double-click to run
3. Start managing your archives immediately

### Option 2: Python Source Code

**Requirements:**
- Python 3.8 or higher
- PyQt5 (`pip install PyQt5`)

**Run:**
```bash
python ZIP-Archive-Manager-v3.2.py
```

## Usage

### GUI Mode
```bash
python ZIP-Archive-Manager-v3.2.py
```

Launch the graphical interface and:
1. Select source files or folders
2. Choose compression settings
3. Specify output location
4. Click "Create Archive" or "Extract"

### Command Line Mode
```bash
# Create archive
python ZIP-Archive-Manager-v3.2.py create <source> <output.zip>

# Extract archive
python ZIP-Archive-Manager-v3.2.py extract <archive.zip> <destination>

# List archive contents
python ZIP-Archive-Manager-v3.2.py list <archive.zip>

# Extract with password
python ZIP-Archive-Manager-v3.2.py extract <archive.zip> <destination> --password <your_password>
```

## Project Files

```
ZIP-Archive-Manager/
├── ZIP-Archive-Manager-v3.2.py    # Main application (Python source code)
├── ZIP-Archive-Manager-v3.2.exe    # Standalone Windows executable
└── README.md                        # This file
```

## Technical Details

### Supported Compression Methods
- **Store**: No compression (fastest)
- **Deflate**: Standard ZIP compression
- **Bzip2**: High compression ratio
- **LZMA**: Maximum compression efficiency

### Supported File Types
- ZIP archives (.zip)
- All file types (documents, images, code, executables, etc.)
- Directories with nested structure preservation

## Security Features

- **Password Protection**: AES encryption support for password-protected archives
- **Integrity Verification**: Built-in checksum validation
- **Safe Extraction**: Protected against directory traversal attacks
- **Permission Handling**: Preserves file permissions on extraction (Unix-like systems)

## Performance

- Handles large files (tested up to 4GB+)
- Optimized memory usage with streaming operations
- Multi-threaded processing for responsive GUI
- Progress indicators for long operations

## Platform Support

| Platform | Supported | Notes |
|----------|-----------|-------|
| Windows  | ✅ Yes    | Full support, .exe version available |
| Linux    | ✅ Yes    | All features available |
| macOS    | ✅ Yes    | All features available |

## Troubleshooting

### Issue: "Module PyQt5 not found"
**Solution**: Install PyQt5 using `pip install PyQt5`

### Issue: "Permission denied" on extraction
**Solution**: Ensure you have write permissions to the destination directory

### Issue: Corrupted ZIP file
**Solution**: Use the "Verify Archive" function to check integrity before extraction

### Issue: .exe won't run on Windows
**Solution**: Ensure Windows 7 or later, or update your system libraries

## About

**Author**: Nady Emad  
**University**: SUT University, Cairo, Egypt  
**Focus**: Cybersecurity & Network Security  
**GitHub**: [@Nady-Emad](https://github.com/Nady-Emad)

This project demonstrates advanced Python programming, cybersecurity principles (data integrity, encryption), and GUI development using PyQt5.

## Version History

### v3.2 (Current)
- Enhanced GUI responsiveness
- Added batch operation support
- Improved error handling
- Added archive verification
- Performance optimizations

### v3.1
- Bug fixes and stability improvements
- Enhanced password protection

### v3.0
- Initial PyQt5 GUI implementation

## License

This project is licensed under the MIT License.

---

**Download & Use**: 
- 🪟 **Windows Users**: Use `ZIP-Archive-Manager-v3.2.exe` (no Python needed)
- 🐧 **Linux/Mac Users**: Use `python ZIP-Archive-Manager-v3.2.py` (requires Python 3.8+)
