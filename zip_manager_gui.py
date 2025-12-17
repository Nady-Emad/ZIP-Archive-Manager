#!/usr/bin/env python3
"""
ZIP Archive Manager - GUI Application Launcher
"""

import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    """Main entry point for GUI application"""
    app = QApplication(sys.argv)
    app.setApplicationName("ZIP Archive Manager")
    app.setApplicationVersion("3.2.0")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
