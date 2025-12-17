import sys
import os
import zipfile
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
QHBoxLayout, QPushButton, QLabel, QFileDialog,
QProgressBar, QTextEdit, QTabWidget, QMessageBox,
QGroupBox, QFileIconProvider, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon, QColor
import time

# ============================================================================
# ZIP ARCHIVE MANAGER - ENHANCED
# ============================================================================

class ZipManager:
    """Unified ZIP archive management with folder support"""

    @staticmethod
    def create_archive(source_path, output_dir):
        """Create ZIP archive from file or folder with complete structure preservation"""
        filename = os.path.basename(source_path.rstrip('/'))
        archive_path = os.path.join(output_dir, f"{filename}.zip")
        
        try:
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.isfile(source_path):
                    # Single file compression
                    zipf.write(source_path, os.path.basename(source_path))
                    
                else:  # Handle folder - ENHANCED with os.walk()
                    # Walk through all directories and files
                    for root, dirs, files in os.walk(source_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Calculate relative path to preserve folder structure
                            arcname = os.path.relpath(file_path, os.path.dirname(source_path))
                            zipf.write(file_path, arcname)
                    
            compressed_size = os.path.getsize(archive_path)
            return archive_path, compressed_size
            
        except Exception as e:
            raise Exception(f"Archive creation failed: {str(e)}")

    @staticmethod
    def extract_archive(archive_path, extract_dir):
        """Extract ZIP archive with folder structure preservation"""
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                zipf.extractall(extract_dir)
                return len(zipf.namelist())
        except Exception as e:
            raise Exception(f"Archive extraction failed: {str(e)}")

    @staticmethod
    def get_archive_info(archive_path):
        """Get archive information"""
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                file_count = len(zipf.namelist())
                compressed_size = os.path.getsize(archive_path)
                uncompressed_size = sum(info.file_size for info in zipf.infolist())
                return file_count, compressed_size, uncompressed_size, zipf.namelist()
        except Exception as e:
            raise Exception(f"Failed to get archive info: {str(e)}")

# ============================================================================
# WORKER THREADS
# ============================================================================

class CompressionWorker(QThread):
    """Worker thread for ZIP compression"""
    
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, source_path, output_dir):
        super().__init__()
        self.source_path = source_path
        self.output_dir = output_dir

    def run(self):
        try:
            start_time = time.time()
            self.progress.emit("Creating ZIP archive...")

            # Ensure absolute paths
            self.source_path = os.path.abspath(self.source_path)
            self.output_dir = os.path.abspath(self.output_dir)

            # Create archive
            archive_path, compressed_size = ZipManager.create_archive(
                self.source_path, self.output_dir
            )

            # Calculate original size
            if os.path.isdir(self.source_path):
                original_size = sum(
                    os.path.getsize(os.path.join(dirpath, filename))
                    for dirpath, dirnames, filenames in os.walk(self.source_path)
                    for filename in filenames
                )
            else:
                original_size = os.path.getsize(self.source_path)

            elapsed_time = time.time() - start_time
            ratio = ((original_size - compressed_size) / original_size * 100) if original_size > 0 else 0

            result = (
                f"✓ ZIP COMPRESSION SUCCESSFUL\n\n"
                f"Original Size: {self._format_size(original_size)}\n"
                f"Compressed Size: {self._format_size(compressed_size)}\n"
                f"Compression Ratio: {ratio:.2f}%\n"
                f"Time Elapsed: {elapsed_time:.2f} seconds\n\n"
                f"Output File: {Path(archive_path).name}"
            )

            self.progress.emit(result)
            self.finished.emit()

        except Exception as e:
            self.error.emit(f"Compression Error: {str(e)}")

    @staticmethod
    def _format_size(bytes_size):
        """Format bytes to human readable size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} TB"


class ExtractionWorker(QThread):
    """Worker thread for ZIP extraction"""
    
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, archive_path, extract_dir):
        super().__init__()
        self.archive_path = archive_path
        self.extract_dir = extract_dir

    def run(self):
        try:
            start_time = time.time()
            self.progress.emit("Extracting ZIP archive...")

            # Get archive info
            file_count, compressed_size, uncompressed_size, files = ZipManager.get_archive_info(
                self.archive_path
            )

            # Extract archive
            file_count = ZipManager.extract_archive(self.archive_path, self.extract_dir)
            elapsed_time = time.time() - start_time

            result = (
                f"✓ ZIP EXTRACTION SUCCESSFUL\n\n"
                f"Archive Size: {self._format_size(compressed_size)}\n"
                f"Extracted Size: {self._format_size(uncompressed_size)}\n"
                f"Files Extracted: {file_count}\n"
                f"Time Elapsed: {elapsed_time:.2f} seconds\n\n"
                f"Location: {Path(self.extract_dir).name}"
            )

            self.progress.emit(result)
            self.finished.emit()

        except Exception as e:
            self.error.emit(f"Extraction Error: {str(e)}")

    @staticmethod
    def _format_size(bytes_size):
        """Format bytes to human readable size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.2f} TB"

# ============================================================================
# REUSABLE UI COMPONENTS
# ============================================================================

class UIComponentFactory:
    """Factory for creating styled UI components"""

    # Color Scheme
    PRIMARY_COLOR = "#1e88e5"
    SUCCESS_COLOR = "#4CAF50"
    INFO_COLOR = "#2196F3"
    ACTION_COLOR = "#FF9800"
    DANGER_COLOR = "#f44336"

    @staticmethod
    def create_button(text, color, callback, width=None):
        """Create styled button"""
        btn = QPushButton(text)
        btn.setFont(QFont('Arial', 11, QFont.Bold))
        btn.clicked.connect(callback)
        if width:
            btn.setMaximumWidth(width)
        
        style = f"""
        QPushButton {{
            background-color: {color};
            color: white;
            padding: 12px 16px;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 11px;
        }}
        QPushButton:hover {{
            background-color: {UIComponentFactory._lighten(color)};
        }}
        QPushButton:pressed {{
            background-color: {UIComponentFactory._darken(color)};
        }}
        """
        btn.setStyleSheet(style)
        return btn

    @staticmethod
    def create_label(text, size=11, bold=False):
        """Create styled label"""
        label = QLabel(text)
        font = QFont('Arial', size)
        font.setBold(bold)
        label.setFont(font)
        return label

    @staticmethod
    def create_group_box(title):
        """Create styled group box"""
        group = QGroupBox(title)
        group.setStyleSheet("""
        QGroupBox {
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 12px;
            font-weight: bold;
            color: #333;
            font-size: 12px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px;
            color: #1e88e5;
        }
        """)
        return group

    @staticmethod
    def create_progress_bar():
        """Create styled progress bar"""
        progress = QProgressBar()
        progress.setStyleSheet("""
        QProgressBar {
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            text-align: center;
            height: 28px;
            background-color: #f5f5f5;
            font-weight: bold;
            font-size: 11px;
        }
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #4CAF50, stop:1 #45a049);
            border-radius: 4px;
        }
        """)
        return progress

    @staticmethod
    def create_text_edit():
        """Create styled text edit"""
        text = QTextEdit()
        text.setReadOnly(True)
        text.setStyleSheet("""
        QTextEdit {
            background-color: #f9f9f9;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            padding: 12px;
            font-family: 'Courier New';
            font-size: 11px;
            color: #333;
        }
        """)
        return text

    @staticmethod
    def _lighten(color):
        """Lighten hex color"""
        return color + "dd"

    @staticmethod
    def _darken(color):
        """Darken hex color"""
        return color[:-2] + "77"

# ============================================================================
# BASE OPERATION WIDGET
# ============================================================================

class BaseOperationWidget(QWidget):
    """Base class for compression and extraction widgets"""

    def __init__(self, title="Operation"):
        super().__init__()
        self.title = title
        self.worker = None
        self.setup_ui()

    def setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        # File selection group
        file_group = UIComponentFactory.create_group_box("Select File/Folder")
        file_layout = self.create_file_selection()
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # Directory selection group
        dir_group = UIComponentFactory.create_group_box("Select Location")
        dir_layout = self.create_directory_selection()
        dir_group.setLayout(dir_layout)
        layout.addWidget(dir_group)

        # Action button
        button_layout = QHBoxLayout()
        self.action_btn = UIComponentFactory.create_button(
            f"▶ {self.title}",
            UIComponentFactory.ACTION_COLOR,
            self.execute_action
        )
        button_layout.addWidget(self.action_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Progress bar
        self.progress = UIComponentFactory.create_progress_bar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        # Results
        results_label = UIComponentFactory.create_label("Results:", 12, True)
        layout.addWidget(results_label)
        self.result_text = UIComponentFactory.create_text_edit()
        self.result_text.setMinimumHeight(200)
        layout.addWidget(self.result_text)

        layout.addStretch()
        self.setLayout(layout)

    def create_file_selection(self):
        """Override in subclass"""
        return QHBoxLayout()

    def create_directory_selection(self):
        """Override in subclass"""
        return QHBoxLayout()

    def execute_action(self):
        """Override in subclass"""
        pass

# ============================================================================
# COMPRESSION WIDGET - FOLDER ONLY
# ============================================================================

class CompressionWidget(BaseOperationWidget):
    """Widget for creating ZIP archives - Folder compression only"""

    def __init__(self):
        self.source_path = None
        self.output_dir = None
        super().__init__("Create Archive")

    def create_file_selection(self):
        """Create folder selection layout - Folder only"""
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        # Button to select folder only
        select_folder_btn = UIComponentFactory.create_button(
            "📁 Browse Folder",
            UIComponentFactory.ACTION_COLOR,
            self.select_folder_only
        )
        btn_layout.addWidget(select_folder_btn)

        # Button to select file only
        select_file_btn = UIComponentFactory.create_button(
            "📄 Browse File Only",
            UIComponentFactory.SUCCESS_COLOR,
            self.select_file_only
        )
        btn_layout.addWidget(select_file_btn)

        btn_layout.addStretch()

        self.file_label = UIComponentFactory.create_label("No selection yet")
        layout.addLayout(btn_layout)
        layout.addWidget(self.file_label)

        return layout

    def create_directory_selection(self):
        """Create directory selection layout"""
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        dir_btn = UIComponentFactory.create_button(
            "📂 Choose Save Location",
            UIComponentFactory.INFO_COLOR,
            self.select_output
        )

        btn_layout.addWidget(dir_btn)
        btn_layout.addStretch()

        self.dir_label = UIComponentFactory.create_label("No selection yet")
        layout.addLayout(btn_layout)
        layout.addWidget(self.dir_label)

        return layout

    def select_folder_only(self):
        """Select only a folder"""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Folder to Compress"
        )

        if folder_path:
            self.source_path = folder_path
            display_name = Path(self.source_path).name
            self.file_label.setText(f"✓ Selected Folder: {display_name}")
            self.file_label.setStyleSheet("color: #4CAF50; font-weight: bold;")

    def select_file_only(self):
        """Select only a file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File to Compress",
            "",
            "All Files (*.*)"
        )

        if file_path:
            self.source_path = file_path
            display_name = Path(self.source_path).name
            self.file_label.setText(f"✓ Selected File: {display_name}")
            self.file_label.setStyleSheet("color: #4CAF50; font-weight: bold;")

    def select_output(self):
        """Select output directory"""
        path = QFileDialog.getExistingDirectory(self, "Choose Save Location")
        if path:
            self.output_dir = path
            display_name = f"Folder: {Path(path).name}"
            self.dir_label.setText(f"✓ Selected: {display_name}")
            self.dir_label.setStyleSheet("color: #2196F3; font-weight: bold;")

    def execute_action(self):
        """Execute compression"""
        if not self.source_path or not self.output_dir:
            QMessageBox.warning(
                self,
                "Incomplete Selection",
                "Please select both folder and save location"
            )
            return

        self.action_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)

        self.worker = CompressionWorker(self.source_path, self.output_dir)
        self.worker.progress.connect(self.update_result)
        self.worker.error.connect(self.handle_error)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def update_result(self, text):
        """Update result display"""
        self.result_text.setText(text)

    def handle_error(self, error):
        """Handle error"""
        QMessageBox.critical(self, "Error", error)
        self.result_text.setText(f"❌ Error:\n{error}")
        self.action_btn.setEnabled(True)
        self.progress.setVisible(False)

    def on_finished(self):
        """Operation finished"""
        self.action_btn.setEnabled(True)
        self.progress.setVisible(False)
        QMessageBox.information(self, "Success", "Archive created successfully! ✓")

# ============================================================================
# EXTRACTION WIDGET
# ============================================================================

class ExtractionWidget(BaseOperationWidget):
    """Widget for extracting ZIP archives"""

    def __init__(self):
        self.archive_path = None
        self.extract_dir = None
        super().__init__("Extract Archive")

    def create_file_selection(self):
        """Create archive file selection layout"""
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        select_btn = UIComponentFactory.create_button(
            "📁 Browse ZIP File",
            UIComponentFactory.SUCCESS_COLOR,
            self.select_archive
        )

        btn_layout.addWidget(select_btn)
        btn_layout.addStretch()

        self.file_label = UIComponentFactory.create_label("No selection yet")
        layout.addLayout(btn_layout)
        layout.addWidget(self.file_label)

        return layout

    def create_directory_selection(self):
        """Create extraction directory selection layout"""
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        dir_btn = UIComponentFactory.create_button(
            "📂 Choose Extract Location",
            UIComponentFactory.INFO_COLOR,
            self.select_extract_dir
        )

        btn_layout.addWidget(dir_btn)
        btn_layout.addStretch()

        self.dir_label = UIComponentFactory.create_label("No selection yet")
        layout.addLayout(btn_layout)
        layout.addWidget(self.dir_label)

        return layout

    def select_archive(self):
        """Select ZIP archive file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select ZIP Archive",
            "",
            "ZIP Files (*.zip);;All Files (*.*)"
        )

        if file_path:
            self.archive_path = file_path
            display_name = Path(file_path).name
            self.file_label.setText(f"✓ Selected: {display_name}")
            self.file_label.setStyleSheet("color: #4CAF50; font-weight: bold;")

    def select_extract_dir(self):
        """Select extraction directory"""
        path = QFileDialog.getExistingDirectory(self, "Choose Extract Location")
        if path:
            self.extract_dir = path
            display_name = Path(path).name
            self.dir_label.setText(f"✓ Selected: {display_name}")
            self.dir_label.setStyleSheet("color: #2196F3; font-weight: bold;")

    def execute_action(self):
        """Execute extraction"""
        if not self.archive_path or not self.extract_dir:
            QMessageBox.warning(
                self,
                "Incomplete Selection",
                "Please select both archive and extraction location"
            )
            return

        self.action_btn.setEnabled(False)
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)

        self.worker = ExtractionWorker(self.archive_path, self.extract_dir)
        self.worker.progress.connect(self.update_result)
        self.worker.error.connect(self.handle_error)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def update_result(self, text):
        """Update result display"""
        self.result_text.setText(text)

    def handle_error(self, error):
        """Handle error"""
        QMessageBox.critical(self, "Error", error)
        self.result_text.setText(f"❌ Error:\n{error}")
        self.action_btn.setEnabled(True)
        self.progress.setVisible(False)

    def on_finished(self):
        """Operation finished"""
        self.action_btn.setEnabled(True)
        self.progress.setVisible(False)
        QMessageBox.information(self, "Success", "Archive extracted successfully! ✓")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

class ZipCompressionApp(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("📦 ZIP Archive Manager")
        self.setGeometry(100, 100, 1100, 800)
        self.setMinimumSize(900, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Apply global stylesheet
        self.setStyleSheet(self.get_global_style())

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header_widget = self.create_header()
        layout.addWidget(header_widget)

        # Tabs
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.addTab(CompressionWidget(), "📦 Create Archive")
        tabs.addTab(ExtractionWidget(), "📂 Extract Archive")
        tabs.addTab(self.create_info_tab(), "ℹ️ Information")

        layout.addWidget(tabs)
        central_widget.setLayout(layout)

    def create_header(self):
        """Create header widget"""
        header = QWidget()
        header.setStyleSheet("""
        QWidget {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #1e88e5, stop:1 #1565c0);
        }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 20, 24, 20)

        title = QLabel("📦 ZIP Archive Manager")
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setStyleSheet("color: white;")

        subtitle = QLabel("Compress and extract folders easily • Full structure support")
        subtitle.setFont(QFont('Arial', 11))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.8);")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        header.setLayout(layout)

        return header

    def create_info_tab(self):
        """Create information tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        info_text = UIComponentFactory.create_text_edit()
        info_text.setText(
            "📚 ZIP Archive Manager v3.2 - FILE & FOLDER COMPRESSION\n\n"
            "═════════════════════════════════════════\n\n"
            "✨ FEATURES:\n"
            "✓ Compress entire folders with complete structure\n"
            "✓ Compress individual files\n"
            "✓ os.walk() for traversing all subdirectories\n"
            "✓ Relative path preservation for hierarchy\n"
            "✓ Extract ZIP archives with folder structure\n"
            "✓ Real-time progress tracking\n"
            "✓ Detailed compression statistics\n\n"
            "HOW TO USE - COMPRESS FOLDER:\n"
            "1. Click 'Create Archive' tab\n"
            "2. Click '📁 Browse Folder' button\n"
            "3. Select the folder you want to compress\n"
            "4. Click '📂 Choose Save Location'\n"
            "5. Select where to save the ZIP file\n"
            "6. Click '▶ Create Archive' button\n"
            "7. Wait for compression to complete\n\n"
            "HOW TO USE - COMPRESS FILE:\n"
            "1. Click 'Create Archive' tab\n"
            "2. Click '📄 Browse File Only' button\n"
            "3. Select the file you want to compress\n"
            "4. Click '📂 Choose Save Location'\n"
            "5. Select where to save the ZIP file\n"
            "6. Click '▶ Create Archive' button\n"
            "7. Wait for compression to complete\n\n"
            "HOW TO USE - EXTRACT ARCHIVE:\n"
            "1. Click 'Extract Archive' tab\n"
            "2. Click '📁 Browse ZIP File' button\n"
            "3. Select the ZIP file to extract\n"
            "4. Click '📂 Choose Extract Location'\n"
            "5. Select extraction destination folder\n"
            "6. Click '▶ Extract Archive' button\n"
            "7. Files extract with original structure\n\n"
            "TECHNICAL DETAILS:\n"
            "• os.walk(source_path) - traverses subdirectories\n"
            "• os.path.relpath() - calculates relative paths\n"
            "• arcname parameter - maintains ZIP structure\n"
            "• ZIP_DEFLATED compression - maximum ratio\n\n"
            "EXAMPLES:\n"
            "MyProject/ folder structure:\n"
            "  ├── src/\n"
            "  │   ├── main.py\n"
            "  │   └── utils.py\n"
            "  ├── data/\n"
            "  │   └── config.json\n"
            "  └── README.txt\n\n"
            "Result: MyProject.zip with exact structure\n\n"
            "═════════════════════════════════════════\n"
            "Built with PyQt5 | OOP Architecture"
        )

        layout.addWidget(info_text)
        widget.setLayout(layout)
        return widget

    @staticmethod
    def get_global_style():
        """Get global application style"""
        return """
        QMainWindow {
            background-color: #f5f5f5;
        }
        QTabWidget::pane {
            border: none;
            background-color: white;
        }
        QTabBar::tab {
            background-color: #e8e8e8;
            color: #333;
            padding: 10px 24px;
            margin-right: 4px;
            border: none;
            font-weight: bold;
            font-size: 11px;
        }
        QTabBar::tab:selected {
            background-color: #1e88e5;
            color: white;
            border-bottom: 3px solid #1565c0;
        }
        QTabBar::tab:hover:!selected {
            background-color: #f0f0f0;
        }
        QMessageBox {
            background-color: white;
        }
        QMessageBox QLabel {
            color: #333;
        }
        QPushButton {
            text-align: center;
        }
        """

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ZipCompressionApp()
    window.show()
    sys.exit(app.exec_())
