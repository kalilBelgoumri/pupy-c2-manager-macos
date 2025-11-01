#!/usr/bin/env python3
"""
Victims Tab - Victim management and command execution
"""

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QSplitter,
    QLabel,
    QMessageBox,
)
from PyQt5.QtCore import Qt, QTimer


class VictimsTab(QWidget):
    """Victims management tab"""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

        # Setup auto-refresh
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_victims)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)

        # ===== Victims List =====
        list_label = QLabel("👥 Connected Victims")
        list_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(list_label)

        self.victims_table = QTableWidget()
        self.victims_table.setColumnCount(6)
        self.victims_table.setHorizontalHeaderLabels(
            ["Client ID", "PID", "User", "OS", "IP", "Status"]
        )
        self.victims_table.itemSelectionChanged.connect(self.on_victim_selected)
        layout.addWidget(self.victims_table)

        # ===== Victim Info & Commands =====
        splitter = QSplitter(Qt.Horizontal)

        # Left: Victim info
        info_layout = QVBoxLayout()
        info_label = QLabel("📋 Victim Info")
        info_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        info_layout.addWidget(info_label)

        self.victim_info_text = QTextEdit()
        self.victim_info_text.setReadOnly(True)
        info_layout.addWidget(self.victim_info_text)

        info_widget = QWidget()
        info_widget.setLayout(info_layout)

        # Right: Command execution
        cmd_layout = QVBoxLayout()
        cmd_label = QLabel("⌨️ Command Execution")
        cmd_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        cmd_layout.addWidget(cmd_label)

        cmd_input_layout = QHBoxLayout()
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText(
            "Enter command (e.g., shell, screenshot, whoami)..."
        )
        execute_btn = QPushButton("Execute")
        execute_btn.clicked.connect(self.execute_command)
        cmd_input_layout.addWidget(self.command_input)
        cmd_input_layout.addWidget(execute_btn)
        cmd_layout.addLayout(cmd_input_layout)

        self.command_output = QTextEdit()
        self.command_output.setReadOnly(True)
        cmd_layout.addWidget(self.command_output)

        cmd_widget = QWidget()
        cmd_widget.setLayout(cmd_layout)

        splitter.addWidget(info_widget)
        splitter.addWidget(cmd_widget)
        splitter.setSizes([400, 600])

        layout.addWidget(splitter)

        # ===== Action Buttons =====
        button_layout = QHBoxLayout()

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_victims)
        button_layout.addWidget(refresh_btn)

        shell_btn = QPushButton("🔌 Open Shell")
        shell_btn.clicked.connect(self.open_shell)
        button_layout.addWidget(shell_btn)

        migrate_btn = QPushButton("💾 Migrate Process")
        migrate_btn.clicked.connect(self.migrate_process)
        button_layout.addWidget(migrate_btn)

        disconnect_btn = QPushButton("❌ Disconnect")
        disconnect_btn.clicked.connect(self.disconnect_victim)
        button_layout.addWidget(disconnect_btn)

        layout.addLayout(button_layout)

    def refresh_victims(self):
        """Refresh victims list"""
        # This would connect to real Pupy listener
        # For now, load mock data
        self.load_mock_victims()

    def load_mock_victims(self):
        """Load mock victims for testing"""
        mock_data = [
            (
                "CLIENT_001",
                "1234",
                "admin@CORP",
                "Windows 10",
                "192.168.1.100",
                "ONLINE",
            ),
            (
                "CLIENT_002",
                "5678",
                "user@CORP",
                "Windows 11",
                "192.168.1.101",
                "ONLINE",
            ),
            (
                "CLIENT_003",
                "9101",
                "guest@CORP",
                "macOS Tahoe",
                "192.168.1.102",
                "OFFLINE",
            ),
        ]

        self.victims_table.setRowCount(len(mock_data))
        for row, (client_id, pid, user, os, ip, status) in enumerate(mock_data):
            self.victims_table.setItem(row, 0, QTableWidgetItem(client_id))
            self.victims_table.setItem(row, 1, QTableWidgetItem(pid))
            self.victims_table.setItem(row, 2, QTableWidgetItem(user))
            self.victims_table.setItem(row, 3, QTableWidgetItem(os))
            self.victims_table.setItem(row, 4, QTableWidgetItem(ip))
            self.victims_table.setItem(row, 5, QTableWidgetItem(status))

    def on_victim_selected(self):
        """Handle victim selection"""
        if self.victims_table.currentRow() >= 0:
            row = self.victims_table.currentRow()
            client_id = self.victims_table.item(row, 0).text()
            pid = self.victims_table.item(row, 1).text()
            user = self.victims_table.item(row, 2).text()
            os = self.victims_table.item(row, 3).text()
            ip = self.victims_table.item(row, 4).text()

            info = f"""Client ID: {client_id}
PID: {pid}
User: {user}
OS: {os}
IP: {ip}

Available Commands:
- shell: Interactive shell
- screenshot: Take screenshot
- download: Download file
- upload: Upload file
- ls: List files
- cd: Change directory
- whoami: Current user
- getprivs: Show privileges
- migrate: Inject into process
- keylogger: Start keylogger"""

            self.victim_info_text.setText(info)
            self.command_output.clear()

    def execute_command(self):
        """Execute command on victim"""
        command = self.command_input.text()
        if not command:
            QMessageBox.warning(self, "Error", "Enter a command first")
            return

        if self.victims_table.currentRow() < 0:
            QMessageBox.warning(self, "Error", "Select a victim first")
            return

        # This would send command to actual victim
        self.command_output.append(f"$ {command}\n")
        self.command_output.append("[*] Sending command to victim...\n")

        # Mock response
        if command == "whoami":
            self.command_output.append("CORP\\admin\n")
        elif command == "screenshot":
            self.command_output.append("[+] Screenshot captured and saved\n")
        elif command == "ls":
            self.command_output.append("Documents/\nDownloads/\nDesktop/\n")
        else:
            self.command_output.append(f"[Output would appear here for: {command}]\n")

        self.command_input.clear()

    def open_shell(self):
        """Open interactive shell"""
        if self.victims_table.currentRow() < 0:
            QMessageBox.warning(self, "Error", "Select a victim first")
            return

        self.command_output.append("\n[+] Interactive shell opened\n")
        self.command_output.append("Type 'exit' to close shell\n\n")

    def migrate_process(self):
        """Migrate to different process"""
        if self.victims_table.currentRow() < 0:
            QMessageBox.warning(self, "Error", "Select a victim first")
            return

        processes = ["explorer.exe", "svchost.exe", "lsass.exe", "services.exe"]
        # Would show dialog to select process
        self.command_output.append(f"[+] Migrating to process...\n")

    def disconnect_victim(self):
        """Disconnect victim"""
        if self.victims_table.currentRow() < 0:
            QMessageBox.warning(self, "Error", "Select a victim first")
            return

        reply = QMessageBox.question(self, "Confirm", "Disconnect this victim?")
        if reply == QMessageBox.Yes:
            self.command_output.append("[+] Disconnecting victim...\n")
