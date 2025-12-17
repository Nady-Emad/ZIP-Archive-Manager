# ZIP Archive Manager

![Version](https://img.shields.io/badge/version-3.2.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-orange)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

Advanced ZIP Archive Manager - Create, extract, and manage ZIP files with ease. Features both GUI & CLI interfaces, password protection, multiple compression methods, batch operations, and comprehensive archive analysis. Built with Python & PyQt5.

## ✨ Features

### Core Features
- **Multiple Interfaces**: Full-featured GUI and powerful CLI
- **Compression Methods**: Support for Store, Deflate, BZIP2, and LZMA compression
- **Password Protection**: Secure your archives with password encryption
- **Batch Operations**: Process multiple archives simultaneously
- **Archive Verification**: Validate archive integrity and CRC checksums
- **Progress Tracking**: Real-time progress indicators for all operations
- **Cross-Platform**: Works on Windows, Linux, and macOS

### GUI Features
- Intuitive tabbed interface
- Drag-and-drop file selection (via browse buttons)
- Real-time archive preview
- Compression method selection with detailed information
- Password strength validation
- Detailed archive statistics
- Batch processing with results summary

### CLI Features
- Complete command-line control
- Scriptable operations
- Batch processing capabilities
- Detailed output and error reporting
- Perfect for automation and scripting

## 📋 Requirements

- Python 3.7 or higher
- PyQt5 5.15.0 or higher (for GUI)

## 🚀 Installation

### Option 1: Install from source

```bash
# Clone the repository
git clone https://github.com/Nady-Emad/ZIP-Archive-Manager.git
cd ZIP-Archive-Manager

# Install dependencies
pip install -r requirements.txt

# Optional: Install as package
pip install -e .
```

### Option 2: Install via pip (when published)

```bash
pip install zip-archive-manager
```

## 💻 Usage

### GUI Application

Launch the graphical interface:

```bash
python zip_manager_gui.py
```

Or if installed as package:

```bash
zip-manager-gui
```

#### GUI Workflow:

1. **Create Archive Tab**:
   - Click "Add Files" or "Add Folder" to select content
   - Choose compression method (Store, Deflate, BZIP2, or LZMA)
   - Optionally enable password protection
   - Click "Browse" to select output location
   - Click "Create Archive"

2. **Extract Archive Tab**:
   - Browse and select ZIP file to extract
   - Choose destination folder
   - Enter password if archive is encrypted
   - Click "Extract Archive"

3. **View Archive Tab**:
   - Select a ZIP file to view
   - Click "View Contents" to see detailed file listing
   - View compression statistics and ratios
   - Click "Verify Archive Integrity" to validate

4. **Batch Operations Tab**:
   - Add multiple archives
   - Batch extract to a common folder
   - Batch verify multiple archives

### CLI Application

The command-line interface provides powerful scripting capabilities:

```bash
python zip_manager_cli.py [command] [options]
```

Or if installed as package:

```bash
zip-manager [command] [options]
```

#### Available Commands:

**Create Archive**:
```bash
# Basic creation
python zip_manager_cli.py create output.zip file1.txt file2.txt folder/

# With LZMA compression
python zip_manager_cli.py create output.zip files/ -c lzma

# With password protection
python zip_manager_cli.py create secure.zip data/ -c deflate -p mypassword
```

**Extract Archive**:
```bash
# Extract to folder
python zip_manager_cli.py extract archive.zip -o output_folder/

# Extract with password
python zip_manager_cli.py extract secure.zip -o output/ -p mypassword

# Extract specific files
python zip_manager_cli.py extract archive.zip -o output/ -m file1.txt file2.txt
```

**List Contents**:
```bash
# Simple listing
python zip_manager_cli.py list archive.zip

# Detailed listing with sizes and compression ratios
python zip_manager_cli.py list archive.zip -d
```

**Verify Archive**:
```bash
# Basic verification
python zip_manager_cli.py verify archive.zip

# Verify with CRC check
python zip_manager_cli.py verify archive.zip --crc
```

**Archive Information**:
```bash
python zip_manager_cli.py info archive.zip
```

**Batch Operations**:
```bash
# Batch extract
python zip_manager_cli.py batch-extract archive1.zip archive2.zip -o output/

# Batch verify
python zip_manager_cli.py batch-verify archive1.zip archive2.zip archive3.zip
```

## 📚 Compression Methods

| Method | Speed | Ratio | CPU Usage | Best For |
|--------|-------|-------|-----------|----------|
| **Store** | Very Fast | None | Very Low | Already compressed files (images, videos) |
| **Deflate** | Fast | Good | Low | General purpose, default choice |
| **BZIP2** | Medium | Better | Medium | Text files, better compression needed |
| **LZMA** | Slow | Best | High | Maximum compression, archival storage |

## 🔐 Security Features

- **Password Protection**: ZIP 2.0 encryption for password-protected archives
- **Password Validation**: Minimum length and strength checking
- **Secure Generation**: Built-in secure password generator
- **Encryption Detection**: Automatic detection of encrypted archives

## 🏗️ Project Structure

```
ZIP-Archive-Manager/
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── zip_manager.py         # Core ZIP operations
│   ├── compression.py         # Compression methods handler
│   ├── security.py            # Password and encryption
│   ├── validators.py          # Archive validation
│   ├── batch_operations.py    # Batch processing
│   └── progress_tracker.py    # Progress tracking
├── gui/                       # GUI components
│   ├── __init__.py
│   └── main_window.py         # Main PyQt5 window
├── cli/                       # CLI components
│   ├── __init__.py
│   └── main.py                # CLI application
├── docs/                      # Documentation
│   ├── API.md                 # API documentation
│   └── USAGE.md               # Detailed usage guide
├── zip_manager_gui.py         # GUI entry point
├── zip_manager_cli.py         # CLI entry point
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
├── setup.py                   # Package setup
└── README.md                  # This file
```

## 🔧 Configuration

Edit `config.py` to customize:

- Default compression method
- Password strength requirements
- UI dimensions
- File size limits
- Batch processing limits

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Bug Reports

Report bugs at: https://github.com/Nady-Emad/ZIP-Archive-Manager/issues

## 👥 Authors

ZIP Archive Manager Team

## 🙏 Acknowledgments

- Built with Python and PyQt5
- Uses standard library zipfile module
- Cross-platform compatibility through Qt framework

## 📸 Screenshots

### GUI Application
The GUI provides an intuitive interface with:
- Tabbed navigation for different operations
- File browser integration
- Real-time progress tracking
- Detailed archive information display
- Batch operation results

### CLI Application
The CLI offers:
- Comprehensive command structure
- Progress bars for long operations
- Detailed output and statistics
- Perfect for automation

## 🔄 Version History

### v3.2.0 (Current)
- Full GUI implementation with PyQt5
- Complete CLI with all major operations
- Multiple compression method support
- Password protection and validation
- Batch operations
- Archive verification
- Cross-platform support
- Comprehensive documentation

## 🚦 Quick Start

### Creating Your First Archive (GUI)
1. Run `python zip_manager_gui.py`
2. Go to "Create Archive" tab
3. Click "Add Files" or "Add Folder"
4. Select compression method
5. Click "Browse" for output location
6. Click "Create Archive"

### Creating Your First Archive (CLI)
```bash
python zip_manager_cli.py create myarchive.zip folder_to_compress/
```

### Extracting an Archive (GUI)
1. Go to "Extract Archive" tab
2. Browse and select ZIP file
3. Select destination folder
4. Click "Extract Archive"

### Extracting an Archive (CLI)
```bash
python zip_manager_cli.py extract myarchive.zip -o extracted_files/
```

## 📞 Support

For support, please:
1. Check the documentation in the `docs/` folder
2. Review existing issues on GitHub
3. Create a new issue if needed

---

**Made with ❤️ using Python and PyQt5**
