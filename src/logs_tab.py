#!/usr/bin/env python3
"""
Logs Tab - Logging and diagnostics
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import Qt
from datetime import datetime
from pathlib import Path


class LogsTab(QWidget):
    """Logs and diagnostics tab"""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)

        # Logs display
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        layout.addWidget(self.logs_text)

        # Buttons
        button_layout = QHBoxLayout()

        clear_btn = QPushButton("🗑️ Clear Logs")
        clear_btn.clicked.connect(self.clear_logs)
        button_layout.addWidget(clear_btn)

        export_btn = QPushButton("💾 Export Logs")
        export_btn.clicked.connect(self.export_logs)
        button_layout.addWidget(export_btn)

        layout.addLayout(button_layout)

        # Add welcome message
        self.add_log("[*] Pupy C2 Manager Started")
        self.add_log("[*] Ready for operations")

    def add_log(self, message):
        """Add message to logs"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}"
        self.logs_text.append(formatted_msg)

        # Keep only last 10000 characters
        doc = self.logs_text.document()
        if doc.toPlainText().__len__() > 10000:
            cursor = self.logs_text.textCursor()
            cursor.select(cursor.Document)
            text = cursor.selectedText()
            cursor.removeSelectedText()
            # Keep last part
            self.logs_text.setText(text[-5000:])

    def clear_logs(self):
        """Clear all logs"""
        self.logs_text.clear()
        self.add_log("[*] Logs cleared")

    def export_logs(self):
        """Export logs to file"""
        from PyQt5.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Logs",
            str(Path.home() / "pupy_logs.txt"),
            "Text Files (*.txt)",
        )

        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(self.logs_text.toPlainText())
                self.add_log(f"[+] Logs exported to {file_path}")
            except Exception as e:
                self.add_log(f"[!] Error exporting logs: {e}")
