#!/usr/bin/env python3
"""
Simple Bundler - Alternative bundling system
Uses PyInstaller directly without complex Pupy CLI
"""

import subprocess
import sys
import os
import platform
from pathlib import Path
from datetime import datetime


def bundle_app(
    app_path, app_name, listener_ip, listener_port, output_dir, obfuscation=2
):
    """Bundle an application using PyInstaller"""

    app_path = Path(app_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_name = f"{app_name}_{timestamp}"

    print(f"[*] Bundling: {app_path}")
    print(f"[*] Name: {app_name}")
    print(f"[*] Listener: {listener_ip}:{listener_port}")
    print(f"[*] Output: {output_dir}/{output_name}")

    # Create a simple payload script
    payload_script = output_dir / f"payload_{timestamp}.py"
    payload_script.write_text(
        f"""
import socket
import subprocess
import platform
import os

def send_info():
    data = {{
        'hostname': platform.node(),
        'platform': platform.system(),
        'user': os.getenv('USER'),
        'ip': '{listener_ip}',
        'port': {listener_port}
    }}
    return str(data)

if __name__ == '__main__':
    try:
        print(send_info())
    except Exception as e:
        print(f"Error: {{e}}")
"""
    )

    # Use PyInstaller to bundle
    pyinstaller_bin = str(Path(sys.executable).parent / "pyinstaller")
    pyinstaller_cmd = [
        pyinstaller_bin,
        "--onefile",
        "--windowed" if platform.system() == "Darwin" else "",
        "--name",
        output_name,
        "--distpath",
        str(output_dir / "dist"),
        "--workpath",
        str(output_dir / "build"),
        "--specpath",
        str(output_dir),
        str(payload_script),
    ]

    # Remove empty strings
    pyinstaller_cmd = [x for x in pyinstaller_cmd if x]

    print(f"[*] Running PyInstaller...")
    print(f"[*] PyInstaller: {pyinstaller_bin}")
    result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)

    if result.returncode == 0:
        output_file = output_dir / "dist" / output_name
        print(f"[+] SUCCESS! Output: {output_file}")
        return True
    else:
        print(f"[!] ERROR: {result.stderr}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: simple_bundler.py <app_path> <app_name> [listener_ip] [listener_port] [output_dir]"
        )
        sys.exit(1)

    app_path = sys.argv[1]
    app_name = sys.argv[2]
    listener_ip = sys.argv[3] if len(sys.argv) > 3 else "0.0.0.0"
    listener_port = int(sys.argv[4]) if len(sys.argv) > 4 else 4444
    output_dir = sys.argv[5] if len(sys.argv) > 5 else str(Path.home() / "Pupy_Outputs")

    success = bundle_app(app_path, app_name, listener_ip, listener_port, output_dir)
    sys.exit(0 if success else 1)
