#!/usr/bin/env python3
"""
Settings Tab - Application configuration
"""

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QCheckBox,
    QPushButton,
    QGroupBox,
    QMessageBox,
    QFileDialog,
)
from PyQt5.QtCore import Qt
from pathlib import Path
import json


class SettingsTab(QWidget):
    """Settings configuration tab"""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)

        # ===== Pupy Configuration =====
        pupy_group = QGroupBox("🎯 Pupy Configuration")
        pupy_layout = QFormLayout()

        pupy_path_layout = QVBoxLayout()
        self.pupy_path_input = QLineEdit()
        self.pupy_path_input.setText(self.parent.config.get("pupy_path", ""))
        browse_pupy_btn = QPushButton("Browse...")
        browse_pupy_btn.clicked.connect(self.browse_pupy)
        pupy_path_layout.addWidget(self.pupy_path_input)
        pupy_path_layout.addWidget(browse_pupy_btn)
        pupy_layout.addRow("Pupy Path:", pupy_path_layout)

        pupy_group.setLayout(pupy_layout)
        layout.addWidget(pupy_group)

        # ===== Listener Configuration =====
        listener_group = QGroupBox("🔌 Listener Configuration")
        listener_layout = QFormLayout()

        self.listener_ip_input = QLineEdit()
        self.listener_ip_input.setText(self.parent.config.get("listener_ip", "0.0.0.0"))
        listener_layout.addRow("Listener IP:", self.listener_ip_input)

        self.listener_port_spinbox = QSpinBox()
        self.listener_port_spinbox.setValue(
            int(self.parent.config.get("listener_port", 4444))
        )
        self.listener_port_spinbox.setMinimum(1)
        self.listener_port_spinbox.setMaximum(65535)
        listener_layout.addRow("Listener Port:", self.listener_port_spinbox)

        listener_group.setLayout(listener_layout)
        layout.addWidget(listener_group)

        # ===== Output Configuration =====
        output_group = QGroupBox("📁 Output Configuration")
        output_layout = QFormLayout()

        output_dir_layout = QVBoxLayout()
        self.output_dir_input = QLineEdit()
        self.output_dir_input.setText(
            self.parent.config.get("output_dir", str(Path.home() / "Pupy_Outputs"))
        )
        browse_output_btn = QPushButton("Browse...")
        browse_output_btn.clicked.connect(self.browse_output)
        output_dir_layout.addWidget(self.output_dir_input)
        output_dir_layout.addWidget(browse_output_btn)
        output_layout.addRow("Output Directory:", output_dir_layout)

        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # ===== Bundler Configuration =====
        bundler_group = QGroupBox("⚙️ Bundler Configuration")
        bundler_layout = QFormLayout()

        self.obfuscation_level_spinbox = QSpinBox()
        self.obfuscation_level_spinbox.setValue(
            int(self.parent.config.get("obfuscation_level", 2))
        )
        self.obfuscation_level_spinbox.setMinimum(0)
        self.obfuscation_level_spinbox.setMaximum(5)
        bundler_layout.addRow(
            "Obfuscation Level (0-5):", self.obfuscation_level_spinbox
        )

        self.auto_test_av_check = QCheckBox("Auto-test with ClamAV after bundling")
        self.auto_test_av_check.setChecked(self.parent.config.get("auto_test_av", True))
        bundler_layout.addRow("", self.auto_test_av_check)

        bundler_group.setLayout(bundler_layout)
        layout.addWidget(bundler_group)

        # ===== Save/Reset Buttons =====
        button_layout = QVBoxLayout()

        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;"
        )
        button_layout.addWidget(save_btn)

        reset_btn = QPushButton("↩️ Reset to Defaults")
        reset_btn.clicked.connect(self.reset_defaults)
        button_layout.addWidget(reset_btn)

        layout.addLayout(button_layout)
        layout.addStretch()

    def browse_pupy(self):
        """Browse for Pupy directory"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Pupy Directory", str(Path.home())
        )
        if dir_path:
            self.pupy_path_input.setText(dir_path)

    def browse_output(self):
        """Browse for output directory"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Output Directory", str(Path.home())
        )
        if dir_path:
            self.output_dir_input.setText(dir_path)

    def save_settings(self):
        """Save settings"""
        self.parent.config = {
            "listener_ip": self.listener_ip_input.text(),
            "listener_port": self.listener_port_spinbox.value(),
            "pupy_path": self.pupy_path_input.text(),
            "output_dir": self.output_dir_input.text(),
            "obfuscation_level": self.obfuscation_level_spinbox.value(),
            "auto_test_av": self.auto_test_av_check.isChecked(),
        }
        self.parent.save_config()
        QMessageBox.information(self, "Success", "Settings saved successfully!")

    def reset_defaults(self):
        """Reset to default settings"""
        reply = QMessageBox.question(self, "Confirm", "Reset all settings to defaults?")
        if reply == QMessageBox.Yes:
            self.parent.config = self.parent.get_default_config()
            self.parent.save_config()
            self.init_ui()
            QMessageBox.information(self, "Success", "Settings reset to defaults!")
