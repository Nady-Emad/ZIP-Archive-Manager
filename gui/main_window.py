"""
PyQt5 GUI Application - Main Window
"""

import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QComboBox, QLineEdit, QFileDialog,
    QMessageBox, QProgressBar, QTabWidget, QTextEdit, QGroupBox,
    QRadioButton, QCheckBox, QSpinBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QStatusBar, QMenuBar, QMenu, QAction
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
import zipfile

# Import utility modules
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.zip_manager import ZIPManager
from utils.compression import CompressionMethod, CompressionHandler
from utils.security import SecurityManager
from utils.validators import ArchiveValidator
from utils.batch_operations import BatchProcessor


class WorkerThread(QThread):
    """Worker thread for long-running operations"""
    progress = pyqtSignal(int, int, str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, operation, *args, **kwargs):
        super().__init__()
        self.operation = operation
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        try:
            result = self.operation(*self.args, **self.kwargs)
            self.finished.emit(True, "Operation completed successfully")
        except Exception as e:
            self.finished.emit(False, str(e))


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.zip_manager = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("ZIP Archive Manager v3.2")
        self.setGeometry(100, 100, 1000, 700)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Create tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Create tabs
        self.create_tab = self.create_create_tab()
        self.extract_tab = self.create_extract_tab()
        self.view_tab = self.create_view_tab()
        self.batch_tab = self.create_batch_tab()
        
        self.tabs.addTab(self.create_tab, "Create Archive")
        self.tabs.addTab(self.extract_tab, "Extract Archive")
        self.tabs.addTab(self.view_tab, "View Archive")
        self.tabs.addTab(self.batch_tab, "Batch Operations")
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_create_tab(self):
        """Create the 'Create Archive' tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # File selection group
        file_group = QGroupBox("Files to Archive")
        file_layout = QVBoxLayout()
        
        # File list
        self.create_file_list = QListWidget()
        file_layout.addWidget(self.create_file_list)
        
        # Buttons for adding/removing files
        btn_layout = QHBoxLayout()
        self.add_files_btn = QPushButton("Add Files")
        self.add_files_btn.clicked.connect(self.add_files_to_archive)
        self.add_folder_btn = QPushButton("Add Folder")
        self.add_folder_btn.clicked.connect(self.add_folder_to_archive)
        self.remove_files_btn = QPushButton("Remove Selected")
        self.remove_files_btn.clicked.connect(self.remove_files_from_archive)
        self.clear_files_btn = QPushButton("Clear All")
        self.clear_files_btn.clicked.connect(self.clear_files_from_archive)
        
        btn_layout.addWidget(self.add_files_btn)
        btn_layout.addWidget(self.add_folder_btn)
        btn_layout.addWidget(self.remove_files_btn)
        btn_layout.addWidget(self.clear_files_btn)
        file_layout.addLayout(btn_layout)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Options group
        options_group = QGroupBox("Archive Options")
        options_layout = QVBoxLayout()
        
        # Compression method
        compression_layout = QHBoxLayout()
        compression_layout.addWidget(QLabel("Compression Method:"))
        self.compression_combo = QComboBox()
        for method in CompressionHandler.get_all_methods():
            self.compression_combo.addItem(
                CompressionHandler.get_compression_name(method),
                method
            )
        self.compression_combo.setCurrentIndex(1)  # Default to Deflate
        compression_layout.addWidget(self.compression_combo)
        options_layout.addLayout(compression_layout)
        
        # Password protection
        password_layout = QHBoxLayout()
        self.password_checkbox = QCheckBox("Password Protection")
        self.password_checkbox.stateChanged.connect(self.toggle_password_field)
        password_layout.addWidget(self.password_checkbox)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setEnabled(False)
        self.password_input.setPlaceholderText("Enter password")
        password_layout.addWidget(self.password_input)
        options_layout.addLayout(password_layout)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Output file
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Output File:"))
        self.create_output_path = QLineEdit()
        self.create_output_path.setPlaceholderText("Select output ZIP file location")
        output_layout.addWidget(self.create_output_path)
        self.browse_output_btn = QPushButton("Browse")
        self.browse_output_btn.clicked.connect(self.browse_output_file)
        output_layout.addWidget(self.browse_output_btn)
        layout.addLayout(output_layout)
        
        # Create button
        self.create_archive_btn = QPushButton("Create Archive")
        self.create_archive_btn.clicked.connect(self.create_archive)
        self.create_archive_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px; font-weight: bold; }")
        layout.addWidget(self.create_archive_btn)
        
        tab.setLayout(layout)
        return tab
    
    def create_extract_tab(self):
        """Create the 'Extract Archive' tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Archive selection
        archive_layout = QHBoxLayout()
        archive_layout.addWidget(QLabel("Archive File:"))
        self.extract_archive_path = QLineEdit()
        self.extract_archive_path.setPlaceholderText("Select ZIP file to extract")
        archive_layout.addWidget(self.extract_archive_path)
        self.browse_archive_btn = QPushButton("Browse")
        self.browse_archive_btn.clicked.connect(self.browse_archive_file)
        archive_layout.addWidget(self.browse_archive_btn)
        layout.addLayout(archive_layout)
        
        # Extract destination
        dest_layout = QHBoxLayout()
        dest_layout.addWidget(QLabel("Extract To:"))
        self.extract_dest_path = QLineEdit()
        self.extract_dest_path.setPlaceholderText("Select destination folder")
        dest_layout.addWidget(self.extract_dest_path)
        self.browse_dest_btn = QPushButton("Browse")
        self.browse_dest_btn.clicked.connect(self.browse_extract_destination)
        dest_layout.addWidget(self.browse_dest_btn)
        layout.addLayout(dest_layout)
        
        # Password
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("Password (if encrypted):"))
        self.extract_password_input = QLineEdit()
        self.extract_password_input.setEchoMode(QLineEdit.Password)
        self.extract_password_input.setPlaceholderText("Enter password if archive is encrypted")
        password_layout.addWidget(self.extract_password_input)
        layout.addLayout(password_layout)
        
        # Extract button
        self.extract_archive_btn = QPushButton("Extract Archive")
        self.extract_archive_btn.clicked.connect(self.extract_archive)
        self.extract_archive_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; padding: 10px; font-weight: bold; }")
        layout.addWidget(self.extract_archive_btn)
        
        layout.addStretch()
        tab.setLayout(layout)
        return tab
    
    def create_view_tab(self):
        """Create the 'View Archive' tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Archive selection
        archive_layout = QHBoxLayout()
        archive_layout.addWidget(QLabel("Archive File:"))
        self.view_archive_path = QLineEdit()
        self.view_archive_path.setPlaceholderText("Select ZIP file to view")
        archive_layout.addWidget(self.view_archive_path)
        self.browse_view_archive_btn = QPushButton("Browse")
        self.browse_view_archive_btn.clicked.connect(self.browse_view_archive)
        archive_layout.addWidget(self.browse_view_archive_btn)
        self.view_archive_btn = QPushButton("View Contents")
        self.view_archive_btn.clicked.connect(self.view_archive)
        archive_layout.addWidget(self.view_archive_btn)
        layout.addLayout(archive_layout)
        
        # Archive info
        self.archive_info_label = QLabel("Archive Information")
        self.archive_info_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(self.archive_info_label)
        
        self.archive_info_text = QTextEdit()
        self.archive_info_text.setReadOnly(True)
        self.archive_info_text.setMaximumHeight(100)
        layout.addWidget(self.archive_info_text)
        
        # Contents table
        self.contents_table = QTableWidget()
        self.contents_table.setColumnCount(5)
        self.contents_table.setHorizontalHeaderLabels(['Name', 'Size', 'Compressed', 'Ratio', 'Type'])
        self.contents_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.contents_table)
        
        # Verify button
        self.verify_archive_btn = QPushButton("Verify Archive Integrity")
        self.verify_archive_btn.clicked.connect(self.verify_archive)
        layout.addWidget(self.verify_archive_btn)
        
        tab.setLayout(layout)
        return tab
    
    def create_batch_tab(self):
        """Create the 'Batch Operations' tab"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Batch operations for processing multiple archives"))
        
        # Archive list
        self.batch_list = QListWidget()
        layout.addWidget(self.batch_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.add_batch_archives_btn = QPushButton("Add Archives")
        self.add_batch_archives_btn.clicked.connect(self.add_batch_archives)
        btn_layout.addWidget(self.add_batch_archives_btn)
        
        self.remove_batch_btn = QPushButton("Remove Selected")
        self.remove_batch_btn.clicked.connect(self.remove_batch_archives)
        btn_layout.addWidget(self.remove_batch_btn)
        
        self.clear_batch_btn = QPushButton("Clear All")
        self.clear_batch_btn.clicked.connect(self.clear_batch_archives)
        btn_layout.addWidget(self.clear_batch_btn)
        layout.addLayout(btn_layout)
        
        # Batch operations
        op_layout = QHBoxLayout()
        self.batch_extract_btn = QPushButton("Batch Extract")
        self.batch_extract_btn.clicked.connect(self.batch_extract)
        op_layout.addWidget(self.batch_extract_btn)
        
        self.batch_verify_btn = QPushButton("Batch Verify")
        self.batch_verify_btn.clicked.connect(self.batch_verify)
        op_layout.addWidget(self.batch_verify_btn)
        layout.addLayout(op_layout)
        
        # Results
        self.batch_results = QTextEdit()
        self.batch_results.setReadOnly(True)
        layout.addWidget(self.batch_results)
        
        tab.setLayout(layout)
        return tab
    
    # Event handlers
    def toggle_password_field(self, state):
        """Toggle password field enabled state"""
        self.password_input.setEnabled(state == Qt.Checked)
    
    def add_files_to_archive(self):
        """Add files to archive list"""
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files to Archive")
        if files:
            self.create_file_list.addItems(files)
    
    def add_folder_to_archive(self):
        """Add folder to archive list"""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder to Archive")
        if folder:
            self.create_file_list.addItem(folder)
    
    def remove_files_from_archive(self):
        """Remove selected files from archive list"""
        for item in self.create_file_list.selectedItems():
            self.create_file_list.takeItem(self.create_file_list.row(item))
    
    def clear_files_from_archive(self):
        """Clear all files from archive list"""
        self.create_file_list.clear()
    
    def browse_output_file(self):
        """Browse for output file location"""
        file, _ = QFileDialog.getSaveFileName(self, "Save Archive As", "", "ZIP Files (*.zip)")
        if file:
            if not file.endswith('.zip'):
                file += '.zip'
            self.create_output_path.setText(file)
    
    def browse_archive_file(self):
        """Browse for archive file to extract"""
        file, _ = QFileDialog.getOpenFileName(self, "Select Archive", "", "ZIP Files (*.zip)")
        if file:
            self.extract_archive_path.setText(file)
    
    def browse_extract_destination(self):
        """Browse for extract destination"""
        folder = QFileDialog.getExistingDirectory(self, "Select Extract Destination")
        if folder:
            self.extract_dest_path.setText(folder)
    
    def browse_view_archive(self):
        """Browse for archive to view"""
        file, _ = QFileDialog.getOpenFileName(self, "Select Archive", "", "ZIP Files (*.zip)")
        if file:
            self.view_archive_path.setText(file)
    
    def add_batch_archives(self):
        """Add archives to batch list"""
        files, _ = QFileDialog.getOpenFileNames(self, "Select Archives", "", "ZIP Files (*.zip)")
        if files:
            self.batch_list.addItems(files)
    
    def remove_batch_archives(self):
        """Remove selected archives from batch list"""
        for item in self.batch_list.selectedItems():
            self.batch_list.takeItem(self.batch_list.row(item))
    
    def clear_batch_archives(self):
        """Clear batch list"""
        self.batch_list.clear()
    
    def create_archive(self):
        """Create a new archive"""
        # Validate inputs
        if self.create_file_list.count() == 0:
            QMessageBox.warning(self, "No Files", "Please add files or folders to archive")
            return
        
        output_path = self.create_output_path.text()
        if not output_path:
            QMessageBox.warning(self, "No Output", "Please specify output file location")
            return
        
        # Get files list
        files = [self.create_file_list.item(i).text() for i in range(self.create_file_list.count())]
        
        # Get compression method
        compression_method = self.compression_combo.currentData()
        
        # Get password
        password = None
        if self.password_checkbox.isChecked():
            password = self.password_input.text()
            if not password:
                QMessageBox.warning(self, "No Password", "Please enter a password or uncheck password protection")
                return
            
            is_valid, msg = SecurityManager.validate_password(password)
            if not is_valid:
                QMessageBox.warning(self, "Invalid Password", msg)
                return
        
        # Progress callback
        def progress_callback(current, total, message):
            if total > 0:
                percentage = int((current / total) * 100)
                self.progress_bar.setValue(percentage)
            self.status_bar.showMessage(message)
        
        # Create archive
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.create_archive_btn.setEnabled(False)
        
        try:
            zip_manager = ZIPManager(progress_callback)
            success = zip_manager.create_archive(
                archive_path=output_path,
                files=files,
                compression_method=CompressionHandler.get_compression_value(compression_method),
                password=password
            )
            
            if success:
                QMessageBox.information(self, "Success", f"Archive created successfully:\n{output_path}")
            else:
                QMessageBox.warning(self, "Failed", "Failed to create archive")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error creating archive:\n{str(e)}")
        
        finally:
            self.progress_bar.setVisible(False)
            self.create_archive_btn.setEnabled(True)
            self.status_bar.showMessage("Ready")
    
    def extract_archive(self):
        """Extract an archive"""
        archive_path = self.extract_archive_path.text()
        if not archive_path:
            QMessageBox.warning(self, "No Archive", "Please select an archive to extract")
            return
        
        extract_path = self.extract_dest_path.text()
        if not extract_path:
            QMessageBox.warning(self, "No Destination", "Please select extraction destination")
            return
        
        password = self.extract_password_input.text() or None
        
        # Progress callback
        def progress_callback(current, total, message):
            if total > 0:
                percentage = int((current / total) * 100)
                self.progress_bar.setValue(percentage)
            self.status_bar.showMessage(message)
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.extract_archive_btn.setEnabled(False)
        
        try:
            zip_manager = ZIPManager(progress_callback)
            success = zip_manager.extract_archive(
                archive_path=archive_path,
                extract_path=extract_path,
                password=password
            )
            
            if success:
                QMessageBox.information(self, "Success", f"Archive extracted successfully to:\n{extract_path}")
            else:
                QMessageBox.warning(self, "Failed", "Failed to extract archive")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error extracting archive:\n{str(e)}")
        
        finally:
            self.progress_bar.setVisible(False)
            self.extract_archive_btn.setEnabled(True)
            self.status_bar.showMessage("Ready")
    
    def view_archive(self):
        """View archive contents"""
        archive_path = self.view_archive_path.text()
        if not archive_path:
            QMessageBox.warning(self, "No Archive", "Please select an archive to view")
            return
        
        try:
            zip_manager = ZIPManager()
            
            # Get archive info
            info = zip_manager.get_archive_info(archive_path)
            if info:
                info_text = f"Files: {info['file_count']}\n"
                info_text += f"Archive Size: {info['archive_size'] / 1024:.2f} KB\n"
                info_text += f"Uncompressed Size: {info['total_uncompressed_size'] / 1024:.2f} KB\n"
                info_text += f"Compression Ratio: {info['compression_ratio']:.1f}%"
                self.archive_info_text.setText(info_text)
            
            # Get contents
            contents = zip_manager.list_contents(archive_path)
            if contents:
                self.contents_table.setRowCount(len(contents))
                for row, item in enumerate(contents):
                    self.contents_table.setItem(row, 0, QTableWidgetItem(item['filename']))
                    self.contents_table.setItem(row, 1, QTableWidgetItem(f"{item['uncompressed_size'] / 1024:.2f} KB"))
                    self.contents_table.setItem(row, 2, QTableWidgetItem(f"{item['compressed_size'] / 1024:.2f} KB"))
                    if item['uncompressed_size'] > 0:
                        ratio = (1 - item['compressed_size'] / item['uncompressed_size']) * 100
                        self.contents_table.setItem(row, 3, QTableWidgetItem(f"{ratio:.1f}%"))
                    else:
                        self.contents_table.setItem(row, 3, QTableWidgetItem("0%"))
                    self.contents_table.setItem(row, 4, QTableWidgetItem(
                        CompressionHandler.get_compression_type_name(item['compression_type'])
                    ))
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error viewing archive:\n{str(e)}")
    
    def verify_archive(self):
        """Verify archive integrity"""
        archive_path = self.view_archive_path.text()
        if not archive_path:
            QMessageBox.warning(self, "No Archive", "Please select an archive to verify")
            return
        
        try:
            is_valid, message = ArchiveValidator.validate_archive(archive_path)
            
            if is_valid:
                QMessageBox.information(self, "Verification Success", f"Archive is valid!\n\n{message}")
            else:
                QMessageBox.warning(self, "Verification Failed", f"Archive validation failed:\n\n{message}")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error verifying archive:\n{str(e)}")
    
    def batch_extract(self):
        """Batch extract archives"""
        if self.batch_list.count() == 0:
            QMessageBox.warning(self, "No Archives", "Please add archives to the batch list")
            return
        
        # Select destination folder
        dest_folder = QFileDialog.getExistingDirectory(self, "Select Batch Extract Destination")
        if not dest_folder:
            return
        
        archives = [self.batch_list.item(i).text() for i in range(self.batch_list.count())]
        
        operations = []
        for archive in archives:
            archive_name = os.path.splitext(os.path.basename(archive))[0]
            extract_path = os.path.join(dest_folder, archive_name)
            operations.append({
                'archive_path': archive,
                'extract_path': extract_path
            })
        
        def progress_callback(current, total, message):
            if total > 0:
                percentage = int((current / total) * 100)
                self.progress_bar.setValue(percentage)
            self.status_bar.showMessage(message)
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        try:
            batch_processor = BatchProcessor(progress_callback)
            results = batch_processor.batch_extract(operations)
            
            results_text = f"Batch Extract Results:\n"
            results_text += f"Total: {results['total']}\n"
            results_text += f"Successful: {results['successful']}\n"
            results_text += f"Failed: {results['failed']}\n\n"
            
            if results['errors']:
                results_text += "Errors:\n" + "\n".join(results['errors'])
            
            self.batch_results.setText(results_text)
            QMessageBox.information(self, "Batch Extract Complete", f"Extracted {results['successful']} of {results['total']} archives")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error in batch extract:\n{str(e)}")
        
        finally:
            self.progress_bar.setVisible(False)
            self.status_bar.showMessage("Ready")
    
    def batch_verify(self):
        """Batch verify archives"""
        if self.batch_list.count() == 0:
            QMessageBox.warning(self, "No Archives", "Please add archives to the batch list")
            return
        
        archives = [self.batch_list.item(i).text() for i in range(self.batch_list.count())]
        
        def progress_callback(current, total, message):
            if total > 0:
                percentage = int((current / total) * 100)
                self.progress_bar.setValue(percentage)
            self.status_bar.showMessage(message)
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        try:
            batch_processor = BatchProcessor(progress_callback)
            results = batch_processor.batch_verify(archives)
            
            results_text = f"Batch Verify Results:\n"
            results_text += f"Total: {results['total']}\n"
            results_text += f"Valid: {results['valid']}\n"
            results_text += f"Invalid: {results['invalid']}\n\n"
            
            if results['errors']:
                results_text += "Errors:\n" + "\n".join(results['errors'])
            
            self.batch_results.setText(results_text)
            QMessageBox.information(self, "Batch Verify Complete", f"Verified {results['valid']} of {results['total']} archives")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error in batch verify:\n{str(e)}")
        
        finally:
            self.progress_bar.setVisible(False)
            self.status_bar.showMessage("Ready")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About ZIP Archive Manager",
            "ZIP Archive Manager v3.2\n\n"
            "A comprehensive ZIP archive management tool with:\n"
            "• Multiple compression methods (Store, Deflate, BZIP2, LZMA)\n"
            "• Password protection\n"
            "• Batch operations\n"
            "• Archive verification\n"
            "• Cross-platform support\n\n"
            "Built with Python and PyQt5"
        )
